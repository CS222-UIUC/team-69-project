import { Link, useNavigate } from 'react-router';
import { useEffect, useRef, useState } from 'react';
import logo from '../assets/logo.png';
import './profile_match.css';
import { z } from 'zod';
import { useQuery, useQueryClient } from '@tanstack/react-query';

const profileSchema = z.object({
  display_name: z.string(),
  major: z.string().max(255),
  year: z.string(),
});

const valid_years = ['freshman', 'sophomore', 'junior', 'senior'];

interface Match {
  id: number;
  display_name: string;
  classes_can_tutor: string[];
  classes_needed: string[];
  major: string;
  year: string;
  rating: string;
}

interface UserData {
  display_name: string;
  classes_can_tutor: string[];
  classes_needed: string[];
  major: string;
  year: string;
}

export default function Profile_Match() {
  //Stuff for adding to lists
  const [classesCanTutorIn, setItems1] = useState<string[]>([]);
  const [input1, setInput1] = useState<string>('');

  const [classesNeeded, setItems2] = useState<string[]>([]);
  const [input2, setInput2] = useState<string>('');

  const displayNameRef = useRef<HTMLInputElement | null>(null);
  const majorRef = useRef<HTMLInputElement | null>(null);
  const yearRef = useRef<HTMLInputElement | null>(null);

  const [enabled, setEnabled] = useState<boolean>(false);

  const queryClient = useQueryClient();
  const navigate = useNavigate();

  const addItem1 = () => {
    const trimmed = input1.trim();
    if (trimmed !== '') {
      setItems1((prev) => [...prev, trimmed]);
      setInput1('');
    }
  };

  const addItem2 = () => {
    const trimmed = input2.trim();
    if (trimmed !== '') {
      setItems2((prev) => [...prev, trimmed]);
      setInput2('');
    }
  };

  const deleteItem1 = (indexToRemove: number) => {
    setItems1((prev) => prev.filter((_, index) => index !== indexToRemove));
  };

  const deleteItem2 = (indexToRemove: number) => {
    setItems2((prev) => prev.filter((_, index) => index !== indexToRemove));
  };

  const handleKeyPress1 = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === 'Enter') {
      e.preventDefault();
      addItem1();
    }
  };

  const handleKeyPress2 = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === 'Enter') {
      e.preventDefault();
      addItem2();
    }
  };

  const {
    data: matches,
    error,
    isLoading,
    refetch,
  } = useQuery({
    queryKey: ['matches'],
    queryFn: async (): Promise<Match[]> => {
      return fetch(`${import.meta.env.VITE_API_BASE}/match/matches`, {
        credentials: 'include',
      }).then((response) => response.json());
    },
    retry: 2,
  });

  const { data: user_data } = useQuery({
    queryKey: ['user-data'],
    queryFn: async (): Promise<UserData> => {
      return fetch(`${import.meta.env.VITE_API_BASE}/user/@me`, {
        credentials: 'include',
      }).then((response) => response.json());
    },
  });

  useEffect(() => {
    if (!user_data) return;
    if (displayNameRef.current)
      displayNameRef.current.value = user_data.display_name;
    if (yearRef.current) yearRef.current.value = user_data.year;
    if (majorRef.current) majorRef.current.value = user_data.major;

    setItems1(user_data.classes_can_tutor);
    setItems2(user_data.classes_needed);
  }, [user_data]);

  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();

    const formData = new FormData(e.currentTarget);
    const data = Object.fromEntries(formData);

    const { success, data: verifiedData } = profileSchema.safeParse(data);
    if (!success) {
      return alert('Signup information is incorrect.');
    }

    if (!valid_years.includes(verifiedData.year.toLowerCase())) {
      return alert(`Year must be one of ${valid_years.join(', ')}.`);
    }

    // temp hack until the input is redone
    const dataToSend: any = { ...verifiedData };
    dataToSend['classes_can_tutor'] = classesCanTutorIn || [];
    dataToSend['classes_needed'] = classesNeeded || [];

    const response = await fetch(`${import.meta.env.VITE_API_BASE}/user`, {
      method: 'PATCH',
      credentials: 'include',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(dataToSend),
    });

    if (response.status != 200) {
      return alert(`Failed to update profile. ${await response.text()}`);
    }

    const match_response = await fetch(
      `${import.meta.env.VITE_API_BASE}/match/new_user`,
      {
        method: 'POST',
        credentials: 'include',
      }
    );
    if (match_response.status != 200) {
      return alert(`Failed to match profile. ${await match_response.text()}`);
    }
    refetch();

    // return alert('Successfully updated profile');
  };

  const handleSubmitSearchByName = async (
    e: React.FormEvent<HTMLFormElement>
  ) => {
    e.preventDefault();

    const formData = new FormData(e.currentTarget);
    const data = Object.fromEntries(formData);

    const response = await fetch(
      `${import.meta.env.VITE_API_BASE}/search?name=${data['display_name']}`,
      {
        // name = request.args.get("name") // search
        method: 'GET',
        credentials: 'include',
      }
    );

    if (response.status != 200) {
      return alert(`Failed to find profile. ${await response.text()}`);
    }

    // alert(await response.json());

    const matched_users: Match[] = await response.json();

    queryClient.setQueriesData(
      { queryKey: ['matches'] },
      (oldData: any) => matched_users
    );

    // return alert('Successfully updated profile');
  };

  return (
    <div className="profile_match">
      <nav className="flex justify-between items-center px-8 py-4 bg-white shadow-md">
        <img src={logo} className="w-32" />
        <ul className="flex space-x-6 text-gray-700">
          <li>
            <Link to={user_data ? '/matches' : '/'} id="link">
              Home
            </Link>
          </li>
          <li>
            <a href="#" id="link">
              Find a Tutor
            </a>
          </li>
          <li>
            <Link to={'/chat'} id="link">
              Messages
            </Link>
          </li>
          <li>
            <a href="#" id="link">
              About Us
            </a>
          </li>
          <li>
            <a href="#" id="link">
              Contact
            </a>
          </li>
        </ul>
        <div className="user-dropdown">
          Username <i className="fas fa-caret-down"></i>
        </div>
      </nav>

      <main className="container text-black w-screen max-w-full">
        <div>
          <form className="profile-section w-full" onSubmit={handleSubmit}>
            <div className="profile-box flex items-center space-x-2">
              <h2 className="h-full pl-2">
                Your Profile
                <button
                  className="fas fa-pen-square"
                  style={{ color: enabled ? 'black' : 'gray' }}
                  onClick={() => setEnabled(!enabled)}
                  type="button"
                ></button>
              </h2>
            </div>
            <img
              className="profile-image"
              src={`https://api.dicebear.com/7.x/bottts/svg?seed=user`}
            ></img>
            <input
              className="inbox"
              name="display_name"
              type="text"
              placeholder="Name:"
              ref={displayNameRef}
              disabled={!enabled}
            />
            <input
              className="inbox"
              name="major"
              type="text"
              placeholder="Major:"
              ref={majorRef}
              disabled={!enabled}
            />
            <input
              className="inbox capitalize"
              name="year"
              type="text"
              placeholder="Year:"
              ref={yearRef}
              disabled={!enabled}
            />
            <div className="input-with-icon">
              <input
                type="text"
                value={input1}
                placeholder="Can tutor in..."
                onChange={(e) => setInput1(e.target.value)}
                onKeyDown={handleKeyPress1}
                disabled={!enabled}
              />
              <i className="fas fa-search"></i>
              <ul>
                {classesCanTutorIn.map((item, index) => (
                  <li
                    key={index}
                    style={{ backgroundColor: enabled ? '#f0f0f0' : '#d3d3d3' }}
                  >
                    {item}
                    <button
                      onClick={() => deleteItem1(index)}
                      className="delete-btn"
                      aria-label={`Delete ${item}`}
                      type="button"
                      disabled={!enabled}
                    >
                      🗑️
                    </button>
                  </li>
                ))}
              </ul>
            </div>
            <div className="input-with-icon">
              <input
                type="text"
                value={input2}
                placeholder="Needs help in..."
                onChange={(e) => setInput2(e.target.value)}
                onKeyDown={handleKeyPress2}
                disabled={!enabled}
              />
              <i className="fas fa-search"></i>
              <ul>
                {classesNeeded.map((item, index) => (
                  <li
                    key={index}
                    style={{ backgroundColor: enabled ? '#f0f0f0' : '#d3d3d3' }}
                  >
                    {item}
                    <button
                      onClick={() => deleteItem2(index)}
                      className="delete-btn"
                      aria-label={`Delete ${item}`}
                      disabled={!enabled}
                    >
                      🗑️
                    </button>
                  </li>
                ))}
              </ul>
            </div>
            {/* <div className="toggle">
                <label>
                  <b>List me as a one-sided tutor</b>
                </label>
                <input type="checkbox" />
              </div> */}
            <button
              className="find-btn mt-5 leading-none"
              type="submit"
              disabled={!enabled}
            >
              Find Matches!
            </button>
          </form>
          <h2 className="text-center text-2xl py-4">OR</h2>
          <form
            className="profile-section w-full"
            onSubmit={handleSubmitSearchByName}
          >
            <div className="search-by-name">
              <input
                type="text"
                name="display_name"
                placeholder="Search by Name"
              />
              <i className="fas fa-search"></i>
            </div>
          </form>
        </div>

        <section className="matches-section">
          <h2>Your Matches</h2>
          <div className="cards">
            {isLoading && <p>Matching in progress...</p>}
            {error && <p>Matched failed.</p>}
            {!isLoading &&
              matches &&
              matches.map((match) => {
                return (
                  <div
                    className="card relative flex flex-col justify-between"
                    key={match.display_name}
                  >
                    <img
                      className="card-img"
                      src={`https://api.dicebear.com/7.x/bottts/svg?seed=${match.id}`}
                    ></img>
                    <div>
                      <h3>{match.display_name}</h3>
                      <p>
                        <strong>Can tutor in:</strong>{' '}
                        {match.classes_can_tutor.join(', ')}
                      </p>
                      <p>
                        <strong>Needs help in:</strong>{' '}
                        {match.classes_needed.join(', ')}
                      </p>
                      <p>
                        <strong>Major:</strong> {match.major}
                      </p>
                      <p className="capitalize">
                        <strong>Year:</strong> {match.year}
                      </p>
                      <p>
                        <strong>Rating:</strong> {match.rating}
                      </p>
                    </div>
                    <button
                      className="chat-btn"
                      onClick={() => {
                        navigate(`/chat?id=${match.id}`);
                      }}
                    >
                      Chat Now!
                    </button>
                  </div>
                );
              })}
          </div>
        </section>
      </main>
    </div>
  );
}
