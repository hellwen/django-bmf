app.filter('mark_safe', ['$sce', function($sce) {
    return function(value) {
        return $sce.trustAsHtml(value);
    }
}]);
