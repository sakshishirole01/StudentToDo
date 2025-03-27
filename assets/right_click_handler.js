document.addEventListener("DOMContentLoaded", function() {
    document.querySelectorAll('.navbar-button').forEach(button => {
        button.addEventListener("contextmenu", function(event) {
            event.preventDefault();
            var subject = event.target.textContent;
            
            // Update Dash Store with subject
            var store = document.getElementById("right-click-data");
            var trigger = document.getElementById("right-click-trigger");

            if (store && trigger) {
                store.setAttribute("data-json", JSON.stringify({"subject": subject}));
                trigger.setAttribute("data-json", JSON.stringify({"trigger": true}));
            }
        });
    });
});
