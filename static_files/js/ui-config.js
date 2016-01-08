/*
 * ui-config
 */

bmfapp.config(['$httpProvider', '$locationProvider', '$logProvider', 'config', function($httpProvider, $locationProvider, $logProvider, config) {
    $httpProvider.defaults.headers.common['X-Requested-With'] = 'XMLHttpRequest';
    $httpProvider.defaults.xsrfCookieName = 'csrftoken';
    $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
    $locationProvider.html5Mode(true).hashPrefix('!');
    $logProvider.debugEnabled(config.debug);
}]);
