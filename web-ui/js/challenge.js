import {
	set_time_button_visible,
	challenge_id,
	server_time_delta,
	show_instance_status, handle_timer, update_timer_div, start_duration, csrf_token
} from "./index"
import ProgressBar from "progressbar.js"

let interval = null
let timedelta = 0

const csrf_token = document.querySelector("base")?.dataset.csrf_token
/**
 * Fetches the API with a formData body {key: value} and CSRF token header and calls onSuccess and onError functions depending on the status of the response
 * @param key
 * @param value
 * @param path
 * @param onSuccess
 * @param onError
 * @returns {Promise<*>}
 */
export async function fetchAPI(key, value, path, onSuccess, onError) {
	const formData = new FormData()
	formData.append(key, value)
	const headers = new Headers()
	headers.append("X-CSRFToken", csrf_token)
	const response = await fetch(path, {
		method: "POST", headers, body: formData
	})
	if (response.ok) {
		const data = await response.json()
		return await onSuccess(data)
	} else {
		return await onError(response)
	}
}

/**
 * Fetches the /challenge route of the API with a formData body {"action": value}
 * @param value
 * @param onSuccess
 * @param onError
 * @returns {Promise<*>}
 */
export async function fetchChallengeAPI(value, onSuccess, onError) {
	return await fetchAPI("action", value, "/challenge/" + challenge_id, onSuccess, onError)
}

/**
 * Fetches the /submit route of the API with a formData body {"flag": flag}
 * @param flag
 * @param step_id
 * @param onSuccess
 * @param onError
 * @returns {Promise<*>}
 */
export async function fetchFlagAPI(flag, step_id, onSuccess, onError) {
	return await fetchAPI("flag", flag, "/submit/" + step_id, onSuccess, onError)
}

export async function start_challenge() {
	document.querySelector("#challenge-status").innerHTML = '<div class="alert alert-primary">The resources of the challenge are currently being provisioned &nbsp;<i class="fa fa-spinner fa-spin"></i></div>'

	// Progress bar
	document.querySelector("#progress-bar").hidden = false
	document.querySelector("#start-btn").disabled = true
	const onSuccess = data => {
		if (data.status === "started" && data.challenge === challenge_id) {
			show_instance_status(data)
			const progress_bar = document.querySelector("#progress-bar")
			progress_bar.hidden = true
			progress_bar.innerHTML = ""
			handle_timer(data.expiration)
			interval = setInterval(function () {
				handle_timer(data.expiration)
			}, 1000)
		} else {
			show_instance_status(data, false)
			const progress_bar = document.querySelector("#progress-bar")
			progress_bar.hidden = true
			progress_bar.innerHTML = ""
		}
	}

	const onError = async response => {
		try {
			const data = await response.json()
			if (data.status === "unauthentified") {
				document.querySelector("#challenge-status").innerHTML = '<div class="alert alert-danger">You need to be authenticated to start a challenge.</div>'
			} else {
				show_instance_status(data, false)
				document.querySelector("#start-btn").disabled = false
				const progress_bar = document.querySelector("#progress-bar")
				progress_bar.hidden = true
				progress_bar.innerHTML = ""
			}
		} catch (e) {
			console.error(e)
		}
	}

	await fetchChallengeAPI("start", onSuccess, onError)
}

export async function status_challenge() {
	const onSuccess = async data => {
		timedelta = server_time_delta(data.server_time)
		show_instance_status(data)
		if (
			data.challenge != null &&
			data.challenge === challenge_id &&
			data.status === "started"
		) {
			clearInterval(interval)
			await handle_timer(data.expiration)
			interval = setInterval(function () {
				handle_timer(data.expiration)
			}, 1000)
		} else {
			update_timer_div(false)
			clearInterval(interval)
		}
	}

	const onError = () => {
		document.querySelector("#challenge-status").innerHTML =
			'<div class="alert alert-danger">Failed to retrieve challenge status.</div>'
	}

	await fetchChallengeAPI("status", onSuccess, onError)
}

export async function stop_challenge(action = "stop") {
	document.querySelector("#challenge-status").innerHTML =
		'<div class="alert alert-primary">The resources of the challenge are currently being unprovisioned &nbsp;<i class="fa fa-spinner fa-spin"></i></div>'
	document.querySelector("#stop-btn").disabled = true
	document.querySelector("#start-btn").disabled = true
	set_time_button_visible(false)
	update_timer_div(false)
	clearInterval(interval)

	const onSuccess = data => {
		document.querySelector("#challenge-status").innerHTML =
			'<div class="alert alert-success">The resources of the challenge have been successfully unprovisioned.</div>'
		show_instance_status(data)
		document.querySelector("#start-btn").disabled = false
	}

	const onError = () => {
		document.querySelector("#stop-btn").disabled = false
		document.querySelector("#start-btn").disabled = true
		document.querySelector("#challenge-status").innerHTML = '<div class="alert alert-danger">Something went wrong.</div>'
	}

	await fetchChallengeAPI(action, onSuccess, onError)
}

	await fetchAPI(action, onSuccess, onError)
}
