$("#execute").click(function (e) {
    e.preventDefault();
    job_id = window.location.href.split('/').slice(-2, -1)[0];
    $.ajax({
        type: "POST",
        url: `/api/job/execute/${job_id}/`,
        data: {
            id: $(this).val(), // < note use of 'this' here
            access_token: $("#access_token").val()
        },
        beforeSend: function () {
            $("#loader").show();
            $("#execute").prop('disabled', true);
            $("#button-text").text("Executing...");
        },
        success: function (result) {
            $("#loader").hide();
            $("#execute").prop('disabled', false);
            $("#button-text").text("Execute Now");
            $(".toast").toast({
                delay: 3000,
                pause_on_hover: false
            });
            $(".toast").toast('show')
        },
        error: function (result) {
            $("#loader").hide();
            $("#execute").prop('disabled', false);
            $("#button-text").text("Execute Now");
            alert('could not execute job');
        },
    });
});