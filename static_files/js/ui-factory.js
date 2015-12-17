/*
 * ui-factory
 */

app.factory('CurrentView', ['$rootScope', '$location', 'PageTitle', function($rootScope, $location, PageTitle) {
    function go(next) {
        $rootScope.bmf_current_view = next;
        if (next && next.type == "list") {
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

        // LIST
        $rootScope.bmf_dashboards.forEach(function(d, di) {
            d.categories.forEach(function(c, ci) {
                c.views.forEach(function(v, vi) {
                    if (prefix + v.url == url) {
                        current = {
                            type: 'list',
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

        // DETAIL
        for (var key in $rootScope.bmf_modules) {
            var module = $rootScope.bmf_modules[key];
            var regex = new RegExp('^' + prefix + module.url + '[0-9]+/$');
            if (regex.test(url)) {
                current = {
                    type: 'detail',
                    module: module,
                };
            }
        }
        if (current) {
            return current;
        }

        return current
    }
    return {get: get, go: go, update: update}
}]);

app.factory('PageTitle', function() {
    var title = '';
    return {
        get: function() { return title; },
        set: function(newTitle) { title = newTitle }
    };
});
