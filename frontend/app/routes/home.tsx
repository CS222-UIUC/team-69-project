import type { Route } from './+types/home';
import { Home_Pg } from '../home_pg/home_pg';
import Profile_Match from '~/profile_match/profile_match';
import Chat_App from '~/chat/chat';

export function meta({}: Route.MetaArgs) {
  return [
    { title: 'TutorSwap' },
    { name: 'description', content: 'Welcome to React Router!' },
  ];
}

export default function Home() {
  return <Home_Pg />;
}
