import { type RouteConfig, index, route } from '@react-router/dev/routes';

export default [
  index('home_pg/home_pg.tsx'),
  route('signup', './sign_up/sign_up.tsx'),
  route('login', './welcome/welcome.tsx'),
  route('matches', './profile_match/profile_match.tsx'),
] satisfies RouteConfig;
