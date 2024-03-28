import Home from "./Home.js";
import Register from "./Register.js";
import Login from "./Login.js";
import Logout from "./Logout.js";
import Profile from "./Profile.js";
import Error from "./Error.js";
import Tournament from "./Tournament.js";
import Online from "./Online.js";
import Local from "./Local.js";
import Games from "./Games.js";

const pathToRegex = path => new RegExp("^" + path.replace(/\//g, "\\/").replace(/:\w+/g, "(.+)") + "$");

const getParams = match => {
    const values = match.result.slice(1);
    const keys = Array.from(match.route.path.matchAll(/:(\w+)/g)).map(result => result[1]);

    return Object.fromEntries(keys.map((key, i) => {
        return [key, values[i]];
    }));
};

const navigateTo = url => {
    history.pushState(null, null, url);
    router();
};

const router = async () => {
    const routes = [
        {   path: "/", view:  Home },
        {   path: "/logout/", view: Logout },
        {   path: "/profile/", view: Profile },
        {   path: "/tournament/", view: Tournament },
        {   path: "/online/", view: Online },
        {   path: "/local/", view: Local },
        {   path: "/error/", view: Error },
        {   path: "/games/", view: Games },
    ];

    // Test each route for potential match
    const potentialMatches = routes.map(route => {
        return {
            route: route,
            result: location.pathname.match(pathToRegex(route.path))
        };
    });

    let match = potentialMatches.find(potentialMatch => potentialMatch.result !== null);
 
    if (!match) {
        match = {
            route: routes[0],
            result: [location.pathname]
        };
    }
 
    const view = new match.route.view(getParams(match));

    document.querySelector("#app").innerHTML = await view.getHtml();
    await view.executeViewScript();
    //Luis m'envoie bon ou pas -> il reste sur la modal ou lui affiche la suite
};

window.addEventListener("popstate", router);

document.addEventListener("DOMContentLoaded", () => {
    document.body.addEventListener("popstate", e => {
        if (e.target.matches("[data-link]")) {
            e.preventDefault();
            navigateTo(e.target.href); 
        }
    });

    router();
});

