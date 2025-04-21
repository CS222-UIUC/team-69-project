import { Link } from 'react-router';
import logo from '../assets/logo.png';
import './profile_match.css';
import { z } from 'zod';
import { useQuery } from '@tanstack/react-query';

const profileSchema = z.object({
  display_name: z.string(),
  major: z.string().max(255),
  year: z.string(),
  classes_can_tutor: z.string().optional(), // both of these will eventually be arrays as input, but that requires a whole new input component
  classes_needed: z.string().optional(),
});

const valid_years = ['freshman', 'sophomore', 'junior', 'senior'];

interface Match {
  display_name: string;
  classes_can_tutor: string[];
  classes_needed: string[];
  major: string;
  year: string;
  rating: string;
}

export default function Profile_Match() {
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
  });

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
    dataToSend['classes_can_tutor'] = [dataToSend['classes_can_tutor']];
    dataToSend['classes_needed'] = [dataToSend['classes_needed']];

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
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(dataToSend),
      }
    );
    if (match_response.status != 200) {
      return alert(`Failed to match profile. ${await match_response.text()}`);
    }
    refetch();

    return alert('Successfully updated profile');
  };

  return (
    <div lang="en">
      <link
        rel="stylesheet"
        href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css"
      />
      <nav className="flex justify-between items-center px-8 py-4 bg-white shadow-md">
        <img src={logo} className="w-32" />
        <ul className="flex space-x-6 text-gray-700">
          <li>
            <a href="#" id="link">
              Home
            </a>
          </li>
          <li>
            <a href="#" id="link">
              Find a Tutor
            </a>
          </li>
          <li>
            <a href="#" id="link">
              Messages
            </a>
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

      <main className="container text-black w-screen">
        <form className="profile-section" onSubmit={handleSubmit}>
          <div className="profile-box">
            <h2>
              Your Profile <i className="fas fa-pen-square"></i>
            </h2>
          </div>
          <div className="profile-image"></div>
          <input
            className="inbox"
            name="display_name"
            type="text"
            placeholder="Name:"
          />
          <input
            className="inbox"
            name="major"
            type="text"
            placeholder="Major:"
          />
          <input
            className="inbox"
            name="year"
            type="text"
            placeholder="Year:"
          />

          <div className="input-with-icon">
            <input
              name="classes_can_tutor"
              type="text"
              placeholder="Can tutor in..."
            />
            <i className="fas fa-search"></i>
          </div>

          <div className="input-with-icon">
            <input
              name="classes_needed"
              type="text"
              placeholder="Needs help in..."
            />
            <i className="fas fa-search"></i>
          </div>

          <div className="toggle">
            <label>
              <b>List me as a one-sided tutor</b>
            </label>
            <input type="checkbox" />
          </div>

          <button className="find-btn" type="submit">
            Find Matches!
          </button>
        </form>

        <section className="matches-section">
          <h2>Your Matches</h2>
          <div className="cards">
            {isLoading && <p>Matching in progress...</p>}
            {error && <p>Matched failed.</p>}
            {!isLoading &&
              matches &&
              matches.map((match) => {
                return (
                  <div className="card" key={match.display_name}>
                    <div className="card-img"></div>
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
                    <p>
                      <strong>Year:</strong> {match.year}
                    </p>
                    <p>
                      <strong>Rating:</strong> {match.rating}
                    </p>
                    <button className="chat-btn">Chat Now!</button>
                  </div>
                );
              })}
          </div>
        </section>
      </main>
    </div>
  );
}
