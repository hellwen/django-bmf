var app = angular.module('djangoBMF', []);
app.config(function($locationProvider) {
    $locationProvider.html5Mode(true).hashPrefix('!');
});
app.config(function($httpProvider) {
    $httpProvider.defaults.headers.common['X-Requested-With'] = 'XMLHttpRequest';
});

// this controller is evaluated first, it gets all
// the data needed to access the bmf's views
app.controller('FrameworkCtrl', function($http, $window, $scope, $location) {

    $scope.django = $window.django;

    // TODO: MOVE TO FACTORY/SERVICE/ETC
    $scope.get_view = function(url) {
        if (url == undefined) {
            url = $location.path();
        }

        var current = null;
        $scope.BMFrameworkViewData.dashboards.forEach(function(d, dindex) {
            d.categories.forEach(function(c, cindex) {
                c.views.forEach(function(v, vindex) {
                    if (v.url == location.pathname) {
                        current = {
                            'view': v,
                            'category': c,
                            'dashboard': d
                        };
                    }
                });
            });
        });
        return current
    }

    var url = $('body').data('api');
    var current_view = null;
    $http.get(url).then(function(response) {
        $scope.BMFrameworkViewData = response.data;
        $scope.$broadcast('BMFrameworkLoaded', $scope.get_view());
    });
});

// This controller updates the dashboard dropdown menu
app.controller('DashboardCtrl', function($scope) {
    $scope.$on('BMFrameworkLoaded', function(event, current_view) {

        $scope.load_dashboard = function(key) {
            $scope.$parent.$broadcast('BMFrameworkUpdateSidebar', key);
            $scope.$parent.$broadcast('BMFrameworkUpdateDashboard', key);
        };

        if (current_view) {
            $scope.load_dashboard(current_view.dashboard.key);
        }
        else {
            $scope.load_dashboard(null);
        }
    });

    $scope.$on('BMFrameworkUpdateDashboard', function(event, key) {
        var response = [];
        var current_dashboard = {};

        $scope.BMFrameworkViewData.dashboards.forEach(function(element, index) {
            var active = false
            if (key == element.key) {
                active = true
                current_dashboard = {
                    'key': element.key,
                    'name': element.name
                }
            }

            response.push({
                'key': element.key,
                'name': element.name,
                'active': active,
            });
        });

        $scope.data = response;
        $scope.current_dashboard = current_dashboard;
    });
});

// This controller updates the dashboard dropdown menu
app.controller('SidebarCtrl', function($scope) {
    $scope.$on('BMFrameworkUpdateSidebar', function(event, key) {

        current_view = $scope.get_view();

        var response = [];
        $scope.BMFrameworkViewData.dashboards.forEach(function(d, dindex) {
            if (key == d.key) {
                response.push({'class': 'sidebar-board', 'name': d.name});
                d.categories.forEach(function(c, cindex) {
                    response.push({'name': c.name});
                    c.views.forEach(function(v, vindex) {
                        if (current_view && c.key == current_view.category.key && v.key == current_view.view.key) {
                            response.push({'name': v.name, 'url': v.url, 'class': 'active'});
                            $scope.$parent.$broadcast('BMFrameworkUpdateView', v, c, d);
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

app.controller('bmfListCtrl', function($scope, $http) {
    $scope.$on('BMFrameworkUpdateView', function(event, view, category, dashboard) {
        var url = view.dataapi + '?d=' + dashboard.key + '&c=' + category.key + '&v=' + view.key
        $http.get(url).then(function(response) {
            $scope.data = response.data;
        });
    });
});
