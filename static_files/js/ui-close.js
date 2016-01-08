(function() {
    var injector = angular.injector(["ng"]);
    var $http = injector.get("$http");
    var apiurl = angular.element.find('body')[0].dataset.api;
    var appurl = angular.element.find('body')[0].dataset.app;

    bmfapp.constant("apiurl", apiurl);
    bmfapp.constant("appurl", appurl);

    $http.get(apiurl).then(function(response){
        bmfapp.constant("config", response.data);

        if (response.data.debug) {
            console.debug("BMF-API", response.data);
        }

        angular.element(document).ready(function() {
            // bootstrap angular
            angular.bootstrap(document, ["djangoBMF"]);
        });
    }, function(response){
        // error handling
        console.error(response);
        alert(gettext('Error!\nCould not load the Application'));
    });
}());

}()); // close ui definition
