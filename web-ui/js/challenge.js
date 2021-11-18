import {
    set_time_button_visible,
    challenge_id,
    server_time_delta,
    show_instance_status, handle_timer, update_timer_div, start_duration
} from "./index"
import ProgressBar from "progressbar.js";

let interval = null
let timedelta = 0

export async function start_challenge() {
    document.querySelector("#challenge-status").innerHTML =
        '<div class="alert alert-primary">The resources of the challenge are currently being provisioned &nbsp;<i class="fa fa-spinner fa-spin"></i></div>'

    // Progress bar
    document.querySelector("#progress-bar").hidden = false;
    const bar = new ProgressBar.Line("#progress-bar", {
        strokeWidth: 2,
        easing: "linear",
        duration: start_duration,
        color: "#78d7fa",
        trailColor: "#eee",
        trailWidth: 1,
        svgStyle: {width: "100%", height: "100%"},
        from: {color: "#87dfff"},
        step: (state, bar) => {
            bar.path.setAttribute("stroke", state.color);
        }
    });

    document.querySelector("#start-btn").disabled = true
    bar.animate(0.9, function () {
        bar.animate(1, {duration: 20000, easing: "linear"});
    });

    // Ajax request
    const formData = new FormData();
    formData.append('action', 'start');
    const response = await fetch("/challenge/" + challenge_id, {
        method: "POST",
        body: formData
    })
    if (response.ok) {
        const data = await response.json()
        if (data.status === "started" && data.challenge === CHALLENGE_ID) {
            bar.stop();
            bar.animate(
                1,
                {duration: 500, to: {width: 1, color: "#63e047"}},
                function () {
                    show_instance_status(data);
                    const progress_bar = $("#progress-bar")[0];
                    progress_bar.hidden = true;
                    progress_bar.innerHTML = "";
                    handle_timer(data.expiration);
                    interval = setInterval(function () {
                        handle_timer(data.expiration);
                    }, 1000);
                }
            );
        } else {
            show_instance_status(data, false);
            bar.stop();
            bar.animate(
                1,
                {duration: 500, to: {width: 1, color: "#E74C3C"}},
                function () {
                    const progress_bar = $("#progress-bar")[0];
                    progress_bar.hidden = true;
                    progress_bar.innerHTML = "";
                }
            );
        }
    } else {
        try {
            const data = await response.json()
            if (data.status === "unauthentified") {
                document.querySelector("#challenge-status").innerHTML =
                    '<div class="alert alert-danger">You need to be authenticated to start a challenge.</div>'
            } else {
                show_instance_status(data, false);
                bar.stop();
                bar.animate(
                    1,
                    {duration: 500, to: {width: 1, color: "#E74C3C"}},
                    function () {
                        document.querySelector("#start-btn").disabled = false;
                        const progress_bar = document.querySelector("#progress-bar")
                        progress_bar.hidden = true;
                        progress_bar.innerHTML = "";
                    }
                );
            }
        } catch (e) {
            console.error(e)
        }
    }

    return false;
}

export async function status_challenge() {
    const formData = new FormData();
    formData.append('action', 'status');
    const response = await fetch("/challenge/" + challenge_id, {
        method: " POST",
        body: formData
    })
    if (response.ok) {
        const data = await response.json()
        timedelta = server_time_delta(data.server_time);
        show_instance_status(data);
        if (
            data.challenge != null &&
            data.challenge === challenge_id &&
            data.status === "started"
        ) {
            clearInterval(interval);
            handle_timer(data.expiration);
            interval = setInterval(function () {
                handle_timer(data.expiration);
            }, 1000);
        } else {
            update_timer_div(false);
            clearInterval(interval);
        }
    } else {
        document.querySelector("#challenge-status").innerHTML =
            '<div class="alert alert-danger">Failed to retrieve challenge status.</div>'
    }
}

export async function stop_challenge(action = "stop") {
    document.querySelector("#challenge-status").innerHTML =
        '<div class="alert alert-primary">The resources of the challenge are currently being unprovisioned &nbsp;<i class="fa fa-spinner fa-spin"></i></div>'
    document.querySelector("#stop-btn").disabled = true;
    document.querySelector("#start-btn").disabled = true;
    set_time_button_visible(false);
    update_timer_div(false);
    clearInterval(interval);
    const formData = new FormData();
    formData.append('action', action);
    const response = await fetch("/challenge/" + challenge_id, {
        method: " POST",
        body: formData
    })
    if (response.ok) {
        const data = await response.json()
        document.querySelector("#challenge-status").innerHTML =
            '<div class="alert alert-success">The resources of the challenge have been successfully unprovisioned.</div>'
        show_instance_status(data);
        document.querySelector("#start-btn").disabled = false;
    } else {
        document.querySelector("#stop-btn").disabled = false;
        document.querySelector("#start-btn").disabled = true;
        document.querySelector("#challenge-status").innerHTML =
            '<div class="alert alert-danger">Something went wrong.</div>'
    }
}
