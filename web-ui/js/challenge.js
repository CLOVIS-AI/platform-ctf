import $ from "jquery";
import {
    timedelta,
    interval,
    set_time_button_visible,
    challenge_id,
    server_time_delta,
    show_instance_status, handle_timer, update_timer_div, start_duration
} from "./index"

export function start_challenge() {
    $("#challenge-status").html(
        '<div class="alert alert-primary">The resources of the challenge are currently being provisioned &nbsp;<i class="fa fa-spinner fa-spin"></i></div>'
    );

    // Progress bar
    $("#progress-bar")[0].hidden = false;
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

    $("#start-btn")[0].disabled = true;
    bar.animate(0.9, function() {
        bar.animate(1, { duration: 20000, easing: "linear" });
    });

    // Ajax request
    $.ajax({
        url: "/challenge/" + challenge_id,
        method: "POST",
        data: { action: "start" },
        success: function(data) {
            if (data.status === "started" && data.challenge === CHALLENGE_ID) {
                bar.stop();
                bar.animate(
                    1,
                    { duration: 500, to: { width: 1, color: "#63e047" } },
                    function() {
                        show_instance_status(data);
                        const progress_bar = $("#progress-bar")[0];
                        progress_bar.hidden = true;
                        progress_bar.innerHTML = "";
                        handle_timer(data.expiration);
                        interval = setInterval(function() {
                            handle_timer(data.expiration);
                        }, 1000);
                    }
                );
            }
            else {
                show_instance_status(data, false);
                bar.stop();
                bar.animate(
                    1,
                    { duration: 500, to: { width: 1, color: "#E74C3C" } },
                    function() {
                        const progress_bar = $("#progress-bar")[0];
                        progress_bar.hidden = true;
                        progress_bar.innerHTML = "";
                    }
                );
            }
        },
        error: function(data) {
            if (data.responseJSON.status === "unauthentified") {
                $("#challenge-status").html(
                    '<div class="alert alert-danger">You need to be authenticated to start a challenge.</div>'
                );
            } else {
                show_instance_status(data.responseJSON, false);
                bar.stop();
                bar.animate(
                    1,
                    { duration: 500, to: { width: 1, color: "#E74C3C" } },
                    function() {
                        $("#start-btn")[0].disabled = false;
                        const progress_bar = $("#progress-bar")[0];
                        progress_bar.hidden = true;
                        progress_bar.innerHTML = "";
                    }
                );
            }
        }
    });

    return false;
}

export function status_challenge() {
    $.ajax({
        url: "/challenge/" + challenge_id,
        method: "POST",
        data: { action: "status" },
        success: function(data) {
            timedelta = server_time_delta(data.server_time);
            show_instance_status(data);
            if (
                data.challenge != null &&
                data.challenge === challenge_id &&
                data.status === "started"
            ) {
                clearInterval(interval);
                handle_timer(data.expiration);
                interval = setInterval(function() {
                    handle_timer(data.expiration);
                }, 1000);
            } else {
                update_timer_div(false);
                clearInterval(interval);
            }
        },
        error: function(data) {
            $("#challenge-status").html(
                '<div class="alert alert-danger">Failed to retrieve challenge status.</div>'
            );
        }
    });
}

export function stop_challenge(action = "stop") {
    $("#challenge-status").html(
        '<div class="alert alert-primary">The resources of the challenge are currently being unprovisioned &nbsp;<i class="fa fa-spinner fa-spin"></i></div>'
    );
    $("#stop-btn")[0].disabled = true;
    $("#start-btn")[0].disabled = true;
    set_time_button_visible(false);
    update_timer_div(false);
    clearInterval(interval);
    $.ajax({
        url: "/challenge/" + challenge_id,
        method: "POST",
        data: { action: action },
        success: function(data) {
            $("#challenge-status").html(
                '<div class="alert alert-success">The resources of the challenge have been successfully unprovisioned.</div>'
            );
            show_instance_status(data);
            $("#start-btn")[0].disabled = false;
        },
        error: function(data) {
            $("#stop-btn")[0].disabled = false;
            $("#start-btn")[0].disabled = true;
            $("#challenge-status").html(
                '<div class="alert alert-danger">Something went wrong.</div>'
            );
        }
    });
}
