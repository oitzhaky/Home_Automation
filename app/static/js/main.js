if ('serviceWorker' in navigator) {
    navigator.serviceWorker.register('/js/sw.js').then(function (registration) {
        // Registration was successful 
        console.log('ServiceWorker registration successful with scope: ', registration.scope);
        registration.pushManager.subscribe({
            userVisibleOnly: true
        }).then(function (subscription) {
            isPushEnabled = true;
            console.log("subscription.subscriptionId: ", subscription.subscriptionId);
            console.log("subscription.endpoint: ", subscription.endpoint);

            // TODO: Send the subscription subscription.endpoint
            // to your server and save it to send a push message
            // at a later date
            $.post('/subscribe', {endpoint:subscription.endpoint}, function(data) {
                alert(data);
            })
            .fail(function() {
                alert("error");
            });
            //return sendSubscriptionToServer(subscription);
        });
    }).catch(function (err) {
        // registration failed :(
        console.log('ServiceWorker registration failed: ', err);
    });
}
