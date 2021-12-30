import {
	challenge_id,
	handle_timer,
	server_time_delta,
	set_time_button_visible,
	show_instance_status,
	update_timer_div
} from "./index"
import {ChallengeData} from "./types"

let interval = null
export let timedelta = 0

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

	// Time left
	const timeLeftElement = document.querySelector("#time-left")
	let timeLeft = parseInt(timeLeftElement.dataset.duration)
	timeLeftElement.hidden = false
	const timeLeftInterval = window.setInterval(() => {
		if (timeLeft >= 0){
			timeLeftElement.innerHTML = `Temps restant estimé : ${timeLeft}s`
			timeLeft--
		} else {
			timeLeftElement.innerHTML = "Temps de provisionnement anormalement long. Merci de patienter."
		}
	}, 1000)

	document.querySelector("#start-btn").disabled = true
	const onSuccess = data => {
		if (data.status === "started" && data.challenge === challenge_id) {
			show_instance_status(data)
			handle_timer(data.expiration)
			interval = setInterval(function () {
				handle_timer(data.expiration)
			}, 1000)
		} else {
			show_instance_status(data, false)

		}
		timeLeftElement.hidden = true
		timeLeftElement.innerHTML = ""
		window.clearInterval(timeLeftInterval)
	}

	const onError = async response => {
		try {
			const data = await response.json()
			if (data.status === "unauthentified") {
				document.querySelector("#challenge-status").innerHTML = '<div class="alert alert-danger">You need to be authenticated to start a challenge.</div>'
			} else {
				show_instance_status(data, false)
				document.querySelector("#start-btn").disabled = false
				timeLeftElement.hidden = true
				timeLeftElement.innerHTML = ""
			}
		} catch (e) {
			console.error(e)
		}
		window.clearInterval(timeLeftInterval)
	}

	await fetchChallengeAPI("start", onSuccess, onError)
}

export async function status_challenge() {
	const onSuccess = async /**ChallengeData*/data => {
		timedelta = server_time_delta(data.server_time)
		show_instance_status(data)
		if (data.challenge !== null && data.challenge === challenge_id && data.status === "started") {
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
		document.querySelector("#challenge-status").innerHTML = '<div class="alert alert-danger">Failed to retrieve challenge status.</div>'
	}

	await fetchChallengeAPI("status", onSuccess, onError)
}

export async function stop_challenge(action = "stop") {
	document.querySelector("#challenge-status").innerHTML = '<div class="alert alert-primary">The resources of the challenge are currently being unprovisioned &nbsp;<i class="fa fa-spinner fa-spin"></i></div>'
	document.querySelector("#stop-btn").disabled = true
	document.querySelector("#start-btn").disabled = true
	set_time_button_visible(false)
	update_timer_div(false)
	clearInterval(interval)

	const onSuccess = data => {
		document.querySelector("#challenge-status").innerHTML = '<div class="alert alert-success">The resources of the challenge have been successfully unprovisioned.</div>'
		show_instance_status(data)
		document.querySelector("#start-btn").disabled = false
	}

	const onError = () => {
		document.querySelector("#stop-btn").disabled = false
		document.querySelector("#start-btn").disabled = true
		document.querySelector("#challenge-status").innerHTML = '<div class="alert alert-danger">Something went wrong.</div>'
	}

	await fetchChallengeAPI("stop", onSuccess, onError)
}

export async function submit_step(step_id, form) {
	const flag = form[0].value

	const onSuccess = data => {
		if (data.status === "failed") {
			alert("Wrong flag!")
		} else if (data.status === "success") {
			const step_card = form.parentElement
			step_card.hidden = true
			step_card.parentElement.classList.add("bg-success")
			step_card.parentElement.classList.add("text-white")

			const step_parent = form.parentElement.parentElement.parentElement
			if (step_parent.classList.contains("card-body")) {
				// This step is inside a section
				let is_completed = true
				step_parent.querySelectorAll(".card").forEach(element => {
					if (!element.classList.contains("bg-success")) {
						is_completed = false
					}
				})

				if (is_completed) {
					step_parent.parentElement.classList.add("section-completed")
					const icon = step_parent.parentElement.parentElement.parentElement.querySelector(".task-dropdown-icon svg")
					icon.classList.remove("fa-circle")
					icon.classList.remove("text-secondary")
					icon.classList.add("fa-check-circle")
					icon.classList.add("text-success")
				}
			}
		}
	}

	const onError = response => {
		console.error(response)
	}
	await fetchFlagAPI(flag, step_id, onSuccess, onError)
}
