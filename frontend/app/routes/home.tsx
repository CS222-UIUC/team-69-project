import type { Route } from './+types/home';
import { Home_Pg } from '../home_pg/home_pg';

export function meta({}: Route.MetaArgs) {
  return [
    { title: 'New React Router App' },
    { name: 'description', content: 'Welcome to React Router!' },
  ];
}

export default function Home() {
  return <Home_Pg />;
}
