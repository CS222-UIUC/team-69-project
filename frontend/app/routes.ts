import { type RouteConfig, index, route, } from '@react-router/dev/routes';


export default [index('routes/home.tsx'),route("signup","./sign_up/sign_up.tsx"),
    route("login","./welcome/welcome.tsx")] satisfies RouteConfig;
