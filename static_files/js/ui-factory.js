/*
 * ui-factory
 */

// This factory uses the rootScope to generate a from a given type (req),
// action(opt) and primary_key(opt)
bmfapp.factory('ApiUrlFactory', ['$rootScope', function($rootScope) {
    return function(type, action, pk) {
        if (!$rootScope.bmf_api.base) throw "api not loaded";
        if (!$rootScope.bmf_api.app_label) throw "no app_label defined";
        if (!$rootScope.bmf_api.model_name) throw "no model_name defined";
        if (!type) throw "no type defined";
        var url = $rootScope.bmf_api.base + 'm/' + $rootScope.bmf_api.app_label + '/' + $rootScope.bmf_api.model_name + '/' + type + '/';
        if (action) url += action + '/';
        if (pk) url += pk + '/';
        return url
    }
}]);

bmfapp.factory('CurrentView', ['$rootScope', '$location', 'PageTitle', function($rootScope, $location, PageTitle) {
    function go(next) {
        $rootScope.bmf_current_view = next;
        if (next && ["list", "detail"].indexOf(next.type) >= 0) {
            PageTitle.set(next.dashboard.name + ' - ' + next.category.name + ' - ' + next.view.name);
            $rootScope.bmf_current_dashboard = {
                key: next.dashboard.key,
                name: next.dashboard.name
            };
        }
    }

    function update(url, prefix) {
        var current = get(url, prefix);
        go(current);
        return current
    }

    function get(url, prefix) {
        if (url == undefined) {
            url = $location.path();
        }
        if (prefix) {
            if ($location.protocol() == 'http' && $location.port() == 80) {
                prefix = 'http://'+ $location.host();
            }
            else if ($location.protocol() == 'https' && $location.port() == 443) {
                prefix = 'https://'+ $location.host();
            }
            else {
                prefix = $location.protocol() + '://' + $location.host() + ':' + $location.port()
            }
        }
        else {
            prefix = ''
        }
        var current = undefined;

        // LIST AND DETAIL
        $rootScope.bmf_dashboards.forEach(function(d, di) {
            d.categories.forEach(function(c, ci) {
                c.views.forEach(function(v, vi) {
                    var regex = new RegExp('^' + prefix + v.url + '([0-9]+)/$');

                    // check if the view relates to a list view
                    if (prefix + v.url == url) {
                        current = {
                            type: 'list',
                            view: v,
                            category: c,
                            dashboard: d,
                        };
                    }

                    // check if the view relates to a detail view
                    if (regex.test(url)) {
                        current = {
                            type: 'detail',
                            module: $rootScope.bmf_modules[v.ct],
                            pk: regex.exec(url)[1],
                            view: v,
                            category: c,
                            dashboard: d,
                        };
                    }
                });
            });
        });
        if (current) {
            return current;
        }
        // Notification index
        if (prefix + url == $rootScope.bmf_ui.notification.url) {
            return {
                type: 'notification',
                module: null,
            }
        }
        if (current) {
            return current;
        }
    }
    return {get: get, go: go, update: update}
}]);

bmfapp.factory('PageTitle', function() {
    var title = '';
    return {
        get: function() { return title; },
        set: function(newTitle) { title = newTitle }
    };
});
