/*
 * ui-run
 */


bmfapp.run(['$rootScope', '$location', '$window', 'ViewUrlconf', function($rootScope, $location, $window, ViewUrlconf) {
    $rootScope.$on('$locationChangeStart', function(event, next, current) {
        if (!ViewUrlconf(next)) {
            // if the url is not managed by the framework, prevent default
            // action from the angularJS url management and redirect browser to the new url
            // if the url was changed
            event.preventDefault(true);
            if (next != current) {
                $window.location = next;
            }
        }
    });
}]);
