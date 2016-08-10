/*
 * ui-config
 */

bmfapp.config(['$httpProvider', '$locationProvider', '$logProvider', 'jwtInterceptorProvider', 'config', function($httpProvider, $locationProvider, $logProvider, jwtInterceptorProvider, config) {
    $httpProvider.defaults.headers.common['X-Requested-With'] = 'XMLHttpRequest';
    $httpProvider.defaults.xsrfCookieName = 'csrftoken';
    $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
    $locationProvider.html5Mode(true).hashPrefix('!');
    $logProvider.debugEnabled(config.debug);
    jwtInterceptorProvider.tokenGetter = ['config', function(config) {
        return localStorage.getItem('bmf_jwt');
    }];
    $httpProvider.interceptors.push('jwtInterceptor');
}]);
