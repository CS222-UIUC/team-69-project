import type { Route } from './+types/home';
import { Welcome } from '../welcome/welcome';
import {Signup} from "../sign_up/sign_up";

export function meta({}: Route.MetaArgs) {
  return [
    { title: 'New React Router App' },
    { name: 'description', content: 'Welcome to React Router!' },
  ];
}

export default function Home() {
  return <Signup />;
}

