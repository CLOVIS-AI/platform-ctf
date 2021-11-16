import $ from "jquery"
import {start_challenge, status_challenge, stop_challenge} from "./challenge";

/* Global variables used in this file (must be defined in the calling page):
 *      SERVER_TIME
 *      CHALLENGE_ID
 *      START_DURATION
 */
export const server_time = SERVER_TIME
export const challenge_id = CHALLENGE_ID
export const start_duration = START_DURATION

export let interval = null
export let timedelta = server_time_delta(server_time)
export let last_check_minutes = 0

const start_button = $("start-btn")
const stop_button = $("stop-btn")
const challenge_timer = $("#chal-timer")

/**
 * Update which buttons are enabled or disabled.
 *
 * For each parameter:
 * - `null` means 'no change'
 * - `true` means 'enable'
 * - `false` means 'disable'
 *
 * @param {boolean|null} enable_start
 * @param {boolean|null} enable_stop
 * @param {boolean|null} visible_time
 */
function update_buttons(enable_start = null, enable_stop = null, visible_time = null) {
    if (enable_start != null)
        start_button.disabled = !enable_start

    if (enable_stop != null)
        stop_button.disabled = !enable_stop

    if (visible_time != null)
        set_time_button_visible(visible_time)
}

/**
 * Display the challenge status message.
 *
 * @param {boolean} handle_buttons
 * @param {boolean} show_spinner
 * @param {string} message
 */
function display_status(handle_buttons, show_spinner = false, message) {
    if (handle_buttons)
        update_buttons(false, false, false)

    $("#challenge-status").html(
        '<div class="alert alert-primary">'+message+' Please wait for the end of this process by <a href="/challenge/' +
        challenge_id +
        '"> refreshing the page</a> regularly. '+(show_spinner ? '&nbsp;<i class="fa fa-spinner fa-spin"></i>' : '')+'</div>'
    );
}

export function show_instance_status(data, handle_buttons = true) {
    // If the ongoing challenge is not the one on the current page
    if (data.challenge != null && data.challenge !== challenge_id) {
        if (data.status === "started" || data.status === "starting") {
            if (handle_buttons)
                update_buttons(false, false, false)

            $("#challenge-status").html(
                '<div class="alert alert-danger">Another instance is already running. Please go to <a href="/challenge/' +
                data.challenge +
                '">the challenge page</a> to stop the previous instance before starting a new one.</div>'
            );
        } else if (data.status === "stopping") {
            display_status(handle_buttons, false, "Another instance is currently stopping.")
        }
    }

    // If this is the page of the ongoing challenge
    else if (data.challenge != null && data.challenge === challenge_id) {
        if (data.status === "started") {
            if (handle_buttons)
                update_buttons(false, true, null)

            $("#challenge-status").html(
                '<div class="alert alert-success">' + data.message + "</div>"
            );
        } else if (data.status === "error") {
            if (handle_buttons)
                update_buttons(true, false, false)

            if (data.message != null) {
                $("#challenge-status").html(
                    '<div class="alert alert-danger">' + data.message + "</div>"
                );
            } else {
                $("#challenge-status").html(
                    '<div class="alert alert-danger">Something went wrong.</div>'
                );
            }
        } else if (data.status === "stopped") {
            if (handle_buttons)
                update_buttons(true, false, false)

            if (data.message != null) {
                $("#challenge-status").html(
                    '<div class="alert alert-danger">' + data.message + "</div>"
                );
            }
        } else if (data.status === "stopping") {
            if (handle_buttons)
                update_buttons(false, false, false)

            $("#challenge-status").html(
                '<div class="alert alert-primary">The resources of the challenge are currently being deprovisioned. Please wait for the end of this process by <a href="/challenge/' +
                challenge_id +
                '"> refreshing the page</a>  regularly &nbsp;<i class="fa fa-spinner fa-spin"></i></div>'
            );
        } else if (data.status === "starting") {
            display_status(handle_buttons, true, "The resources of the challenge are currently being provisioned.")

            if (handle_buttons)
                update_buttons(false, false, false)

            $("#challenge-status").html(
                '<div class="alert alert-primary">The resources of the challenge are currently being provisioned. Please wait for the end of this process by <a href="/challenge/' +
                challenge_id +
                '"> refreshing the page</a>  regularly </div>'
            );
        }
    }
}

function extend_time() {
    $.ajax({
        url: "/challenge/" + challenge_id,
        method: "POST",
        data: {action: "extend"},
        success: function (data) {
            if (data.status === "extended") {
                status_challenge();
            }
        },
        error: function (data) {
            alert("Time not extended : error (?)");
        }
    });
}

/**
 * Make the time button visible or invisible.
 *
 * @param {boolean} visible
 */
export function set_time_button_visible(visible) {
    if (visible && !$("#extend-btn").length) {
        // The button does not exists and needs to be created
        $("#chal-btn-group").append(
            "<button id='extend-btn' class='btn btn-primary shadow-none' title='Add one hour before expiration'>Extend time</button>"
        );
        $("#extend-btn").click(function () {
            extend_time();
        });
    } else if (!visible && $("#extend-btn").length) {
        // The button does exists and needs to be removed
        $("#extend-btn").remove();
    }
}

export function update_timer_div(visible, text = "", color = "grey") {
    if (!visible) {
        if (!challenge_timer.hasClass("d-none")) {
            challenge_timer.addClass("d-none");
        }
        return;
    }

    if (visible && challenge_timer.hasClass("d-none")) {
        challenge_timer.removeClass("d-none");
    }

    challenge_timer.removeClass("badge-secondary");
    challenge_timer.removeClass("badge-warning");
    challenge_timer.removeClass("badge-danger");

    if (color === "grey") challenge_timer.addClass("badge-secondary");
    if (color === "yellow") challenge_timer.addClass("badge-warning");
    if (color === "red") challenge_timer.addClass("badge-danger");

    challenge_timer.text(text);
}

/**
 * @param {string} server_time
 * @returns {number} (seconds)
 */
export function server_time_delta(server_time) {
    let server_time_seconds = Date.parse(server_time) / 1000;
    const client_time = new Date().getSeconds();
    return server_time_seconds - client_time;
}

/**
 * @param {string} end_time
 */
export function handle_timer(end_time) {
    const endTime = Date.parse(end_time) / 1000;

    let now = new Date().getSeconds();

    const timeLeft = endTime - now + timedelta;

    if (timeLeft < 0) {
        set_time_button_visible(false);
        update_timer_div(true, "00m 00s", "red");
        clearInterval(interval);
        stop_challenge("timeout");
        return;
    }

    let color = "grey";
    if (timeLeft < 300) color = "red";
    else if (timeLeft < 600) color = "yellow";

    const days = Math.floor(timeLeft / 86400);
    const hours = Math.floor((timeLeft - days * 86400) / 3600);
    let minutes = Math.floor((timeLeft - days * 86400 - hours * 3600) / 60);
    let seconds = Math.floor(timeLeft - days * 86400 - hours * 3600 - minutes * 60);
    const saved_minutes = seconds === 0 ? minutes : -1;

    let text = "";
    if (hours > 0) {
        text = hours + "h ";
    }
    if (minutes < "10") {
        minutes = "0" + minutes;
    }
    text = text + minutes + "m ";
    if (seconds < "10") {
        seconds = "0" + seconds;
    }
    text = text + seconds + "s";

    set_time_button_visible(timeLeft < 3600)
    update_timer_div(true, text, color);

    // Every minute, the status of the challenge is updated to re-synchronize
    // the remaining time or detect that the instance has been stopped
    if (saved_minutes !== -1 && saved_minutes !== last_check_minutes) {
        last_check_minutes = saved_minutes;
        status_challenge();
    }
}

start_button.click(start_challenge);
stop_button.click(stop_challenge);
status_challenge();
