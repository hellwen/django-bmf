var app = angular.module('djangoBMF', []);
app.config(['$httpProvider', function($httpProvider) {
    $httpProvider.defaults.headers.common['X-Requested-With'] = 'XMLHttpRequest';
}]);

// this controller is evaluated first, it gets all
// the data needed to access the bmf's views
app.controller('FrameworkCtrl', function($http, $scope) {
    var url = $('body').data('api');
    var current_view = null;
    $http.get(url).then(function(response) {
        response.data.dashboards.forEach(function(d, dindex) {
            d.categories.forEach(function(c, cindex) {
                c.views.forEach(function(v, vindex) {
                    if (v.url == location.pathname) {
                        current_view = {
                            'view': v,
                            'category': c,
                            'dashboard': d
                        };
                    }
                });
            });
        });
        $scope.BMFrameworkViewData = response.data;
        $scope.$broadcast('BMFrameworkLoaded', current_view);
    });
});

// This controller updates the dashboard dropdown menu
app.controller('DashboardCtrl', function($scope) {
    $scope.$on('BMFrameworkLoaded', function(event, current_view) {
        var response = [];
        $scope.BMFrameworkViewData.dashboards.forEach(function(element, index) {
            if (current_view && current_view.dashboard.key == element.key) {
                response.push({'key': element.key, 'name': element.name, 'active': true, 'url': element.url});
            }                                        
            else {                                   
                response.push({'key': element.key, 'name': element.name, 'active': false, 'url': element.url});
            }
        });
        $scope.data = response;
        $scope.load_dashboard = function(arg) {alert(arg)};
    });
});

// This controller updates the dashboard dropdown menu
app.controller('SidebarCtrl', function($scope) {
    $scope.$on('BMFrameworkLoaded', function(event, current_view) {
        var response = [];
        $scope.BMFrameworkViewData.dashboards.forEach(function(d, dindex) {
            if (current_view && current_view.dashboard.key == d.key) {
                response.push({'class': 'sidebar-board', 'name': d.name});
                d.categories.forEach(function(c, cindex) {
                    response.push({'name': c.name});
                    c.views.forEach(function(v, vindex) {
                        if (c.key == current_view.category.key && v.key == current_view.view.key) {
                            response.push({'name': v.name, 'url': v.url, 'class': 'active'});
                        }
                        else {
                            response.push({'name': v.name, 'url': v.url});
                        }
                    });
                });
            }
        });
        $scope.data = response;
    });
});
