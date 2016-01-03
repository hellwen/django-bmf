/*
 * ui-controller
 */

// this controller is evaluated first, it gets all
// the data needed to access the bmf's views
bmfapp.controller('FrameworkCtrl', ['$http', '$rootScope', '$scope', '$window', 'ViewUrlconf', function($http, $rootScope, $scope, $window, ViewUrlconf) {

    /**
     * @description
     *
     * This scope stores the base url to the API (needed for lookups)
     *
     */
    $rootScope.bmf_api_base = angular.element.find('body')[0].dataset.api;

    /**
     * @description
     *
     * This scope stores the currently active module
     *
     */
    $rootScope.bmf_module = undefined;

    /**
     * @description
     *
     * Every overlay get appended to this list. we only show one modal
     * per time and update the content as long as this list is not empty
     *
     * data
     * - TODO??
     *
     */
    $rootScope.bmf_modal = [];

    /**
     * @description
     *
     * The breadcrumbs are filled with data as the user navigates through the
     * framework. it contains information about the history to provide the
     * functionality to go back one page. With this we are able to travel
     * from a module to another without changing the overlaying view.
     * 
     * The listing pages overwrite this, while every detail-page appends to
     * this.
     *
     * data is generated via the ViewUrlconf factory
     * - name: the view callback name
     * - url: the called url
     * - kwargs: the views keyword arguments
     *
     */
    $rootScope.bmf_breadcrumbs = [];

    /**
     * @description
     *
     * The urlconf is needed to map an url to a view / controller (?)
     * TODO: check if if could be loaded via the REST-API
     *
     */
    $rootScope.bmf_view_urlconf = [
        {
            name: 'list',
            parent: null,
            regex: new RegExp('dashboard/([\\w-]+)/([\\w-]+)/([\\w-]+)/$'),
            args: ['dashboard', 'category', 'view'],
        },
        {
            name: 'detail',
            parent: 'list',
            regex: new RegExp('dashboard/([\\w-]+)/([\\w-]+)/([\\w-]+)/([0-9]+)/$'),
            args: ['dashboard', 'category', 'view', 'pk'],
        },
        {
            name: 'notification',
            parent: null,
            regex: new RegExp('notification/$'),
            args: [],
        },
        {
            name: 'notification',
            parent: null,
            regex: new RegExp('notification/([\\w-]+)/([\\w-]+)/$'),
            args: ['app_label', 'model_name'],
        },
        {
            name: 'detail',
            parent: 'notification',
            regex: new RegExp('notification/([\\w-]+)/([\\w-]+)/([0-9]+)/$'),
            args: ['app_label', 'model_name', 'pk'],
        },
    ];
    // TODO this is currenty unused
    $rootScope.bmf_api_urlconf = [
    ];

    /**
     * @description
     *
     * Event broadcaster
     *
     */
    $rootScope.bmfevent_activity = function() {
        // TODO
        $rootScope.$broadcast(BMFEVENT_ACTIVITY);
    }
    $rootScope.bmfevent_content = function(name) {
        var crumbs = $rootScope.bmf_breadcrumbs;
        if (!crumbs || crumbs.length == 0 || crumbs[crumbs.length - 1].name != name) {
            $rootScope.$broadcast(BMFEVENT_CONTENT, name)
        }
    }
    $rootScope.bmfevent_dashboard = function(key) {
        $rootScope.$broadcast(BMFEVENT_DASHBOARD, key);
    }
    $rootScope.bmfevent_data = function() {
        // TODO
        $rootScope.$broadcast(BMFEVENT_DATA);
    }
    $rootScope.bmfevent_modal = function() {
        // TODO
        $rootScope.$broadcast(BMFEVENT_MODAL);
    }
    $rootScope.bmfevent_navigation = function() {
        // TODO
        $rootScope.$broadcast(BMFEVENT_NAVIGATION);
    }
    $rootScope.bmfevent_sidebar = function(dashboard_key) {
        $rootScope.bmf_dashboards.forEach(function(d, i) {
            if (d.key == dashboard_key) {
                $rootScope.$broadcast(BMFEVENT_SIDEBAR, d.key, d.name);
            }
        });
    }

    // pace to store basic templates
    /**
     * @description
     *
     * place where all templates are stored
     *
     */
    $rootScope.bmf_templates = {
        'list': '',
        'detail': '',
        'notification': '',
    };


    $rootScope.bmf_api = {
        base: angular.element.find('body')[0].dataset.api,
        app_label: undefined,
        model_name: undefined,
        module: undefined,
    };

    // place to store all dashboards
    $rootScope.bmf_dashboards = undefined;

    // place to store all top navigation
    $rootScope.bmf_navigation = undefined;

    // place to store all sitemaps
    $rootScope.bmf_sidebars = undefined;

    $rootScope.bmf_modules = undefined;

    $rootScope.bmf_ui = undefined;

    $rootScope.bmf_last_dashboard = undefined;
    $rootScope.bmf_last_view = undefined;

    // Load data from REST API
    var url = angular.element.find('body')[0].dataset.api;
    $http.get(url).then(function(response) {
        // Update sidebar and Dashboard objects
        var sidebar = {}
        response.data.dashboards.forEach(function(element, index) {
            sidebar[element.key] = element.categories;
        });

        var modules = {}
        response.data.modules.forEach(function(element, index) {
            modules[element.ct] = element;
        });

        $rootScope.bmf_modules = modules;
        $rootScope.bmf_sidebars = sidebar;

        $rootScope.bmf_ui = response.data.ui;
        $rootScope.bmf_dashboards = response.data.dashboards;
        $rootScope.bmf_debug = response.data.debug;
        $rootScope.bmf_templates = response.data.templates;
        $rootScope.bmf_navigation = response.data.navigation;

        if ($rootScope.bmf_debug) {
            console.log("BMF-API", response.data);
        }
        $rootScope.bmfevent_dashboard();

        // load urlconf when all variables are set
        ViewUrlconf(window.location.href);
    });

}]);


// bmfapp.controller('ModalCtrl', [function() {
// }]);


// This controller updates the dashboard dropdown menu
bmfapp.controller('SidebarCtrl', ['$scope', '$rootScope', function($scope, $rootScope) {
    $scope.$on(BMFEVENT_SIDEBAR, function(event, key, name) {update(key, name)});

    $scope.data = [];

    function update(key, name) {
        var root = $rootScope.bmf_breadcrumbs[0];
        dashboard(root, key, name);
    }

    function dashboard(root, key, name) {
        var data = []
        data.push({
            'class': 'sidebar-board',
            'name': name,
        });

        $rootScope.bmf_sidebars[key].forEach(function(c, ci) {
            data.push({'name': c.name});
            c.views.forEach(function(v, vi) {
                if (root && 'dashboard' in root.kwargs && 'category' in root.kwargs && 'view' in root.kwargs && root.kwargs.dashboard == key && root.kwargs.category == c.key && root.kwargs.view == v.key) {
                    data.push({'name': v.name, 'url': v.url, 'class': 'active'});
                }
                else {
                    data.push({'name': v.name, 'url': v.url});
                }
            });
        });
        $scope.data = data;
    }
}]);


// This controller updates the dashboard dropdown menu
bmfapp.controller('DashboardCtrl', ['$scope', '$rootScope', function($scope, $rootScope) {

    $scope.$on(BMFEVENT_DASHBOARD, function(event, key) {update(key)});

    $scope.data = [];
    $scope.current = undefined;

    function update(key) {
        var response = [];
        var data = [];
        var current = undefined;

        $rootScope.bmf_dashboards.forEach(function(d, di) {
            var active = false
            if (key == d.key) {
                active = true;
                current = d;
            }
            data.push({
                'key': d.key,
                'name': d.name,
                'active': active,
            });
        });

        // fire event
        if (current) {
            $rootScope.bmfevent_sidebar(key);
        }

        $scope.data = data;
        $scope.current = current;
    }
    $scope.update = update;
}]);


// This controller updates the dashboards navigation
bmfapp.controller('NavigationCtrl', ['$scope', '$interval', '$http', function($scope, $interval, $http) {
    $scope.data = undefined;

    $scope.$watch(
        function(scope) {return scope.bmf_navigation && scope.bmf_navigation.length || 0},
        function(newValue) {if (newValue != undefined) init_navigation()}
    );

    $scope.$on('$destroy', function() {
        // Make sure that the interval is destroyed too
        $scope.data.forEach(function(nav, i) {
            if (nav.timer) {
                $interval.cancel(nav.timer);
            }
        });
    });

    function init_navigation() {
        if (!$scope.bmf_navigation) return false;

        $scope.data = $scope.bmf_navigation;

        $scope.update = function (i) {
            nav = $scope.data[i];
            // console.log("TIMER", i, nav)
            $http({
                method: 'GET',
                url: nav.api,
                headers: {
                    'Content-Type': 'application/json'
                },
            }).then(function (response) {
                // success callback
                // console.log("success", this, response);
                $scope.data[i].active = response.data.active;
                $scope.data[i].count = response.data.count;
            }, function (response) {
                // error callback
                console.log("Navigation Timer Error", response);
            });
        }

        $scope.data.forEach(function(nav, i) {
            // use the button as a link if url is set
            if (nav.url == undefined) nav.url = '#';

            // stop an old timer
            if (nav.timer) {
                $interval.cancel(nav.timer);
            }
            nav.timer = undefined;
            nav.active = false;
            nav.count = 0;

            if (nav.api && nav.intervall) {
                $scope.update(i);
                nav.timer = $interval(function() {
                    $scope.update(i)
                }, nav.intervall * 1000);
            }
        });
    }
}]);


// bmfapp.controller('ContentCtrl', [function() {
// }]);


// bmfapp.controller('DataCtrl', [function() {
// }]);


// bmfapp.controller('PaginationCtrl', [function() {
// }]);


bmfapp.controller('ActivityCtrl', ['$scope', '$http', function($scope, $http) {
    $scope.data = {};
    $scope.processForm = function() {
        var url = $scope.$parent.$parent.ui.views.activity.url;
        $http({
            method: 'POST',
            data: $scope.data,
            url: url,
            headers: {
                'Content-Type': 'application/json'
            },
        }).then(function (response) {
            // success callback
            // console.log("success", this, response);
            window.location.reload(); 
        }, function (response) {
            // error callback
            console.log("ActivityForm - Error", response);
            alert(response.data.non_field_errors[0]);
        });
    }
}]);


/*
 * View specific controller
 */


// bmfapp.controller('ListViewCtrl', [function() {
// }]);


// bmfapp.controller('DetailViewCtrl', [function() {
// }]);


// bmfapp.controller('NotificationViewCtrl', ['$scope', '$rootScope', function($scope, $rootScope) {
// }]);
