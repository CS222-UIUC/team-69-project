import { Link } from 'react-router';
import logo from '../assets/logo.png';
import './profile_match.css';
import { z } from 'zod';

const profileSchema = z.object({
  display_name: z.string(),
  major: z.string().max(255),
  year: z.string(),
  classes_can_tutor: z.string().optional(), // both of these will eventually be arrays as input, but that requires a whole new input component
  classes_needed: z.string().optional(),
});

const valid_years = ['freshman', 'sophomore', 'junior', 'senior'];

export default function Profile_Match() {
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

      <main className="container text-black">
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
            <div className="card">
              <div className="card-img"></div>
              <h3>A. R.</h3>
              <p>
                <strong>Can tutor in:</strong> CS 128, CS 225
              </p>
              <p>
                <strong>Needs help in:</strong> ECON 203
              </p>
              <p>
                <strong>Major:</strong> CS + Statistics
              </p>
              <p>
                <strong>Year:</strong> Sophomore
              </p>
              <p>
                <strong>Rating:</strong> 4.8
              </p>
              <button className="chat-btn">Chat Now!</button>
            </div>
            <div className="card">
              <div className="card-img"></div>
              <h3>C. A.</h3>
              <p>
                <strong>Can tutor in:</strong> ECE 220
              </p>
              <p>
                <strong>Needs help in:</strong> CHEM 360
              </p>
              <p>
                <strong>Major:</strong> Electrical Engineering
              </p>
              <p>
                <strong>Year:</strong> Freshman
              </p>
              <p>
                <strong>Rating:</strong> 4.6
              </p>
              <button className="chat-btn">Chat Now!</button>
            </div>
            <div className="card">
              <div className="card-img"></div>
              <h3>A. U.</h3>
              <p>
                <strong>Can tutor in:</strong> ADV 281, ADV 150
              </p>
              <p>
                <strong>Needs help in:</strong> CS 173
              </p>
              <p>
                <strong>Major:</strong> Advertising
              </p>
              <p>
                <strong>Year:</strong> Freshman
              </p>
              <p>
                <strong>Rating:</strong> 4.8
              </p>
              <button className="chat-btn">Chat Now!</button>
            </div>
            <div className="card">
              <div className="card-img"></div>
              <h3>Y. G.</h3>
              <p>
                <strong>Can tutor in:</strong> PSYC 248
              </p>
              <p>
                <strong>Needs help in:</strong> MATH 231, PHYS 212
              </p>
              <p>
                <strong>Major:</strong> CS + Psychology
              </p>
              <p>
                <strong>Year:</strong> Senior
              </p>
              <p>
                <strong>Rating:</strong> 4.7
              </p>
              <button className="chat-btn">Chat Now!</button>
            </div>
          </div>
        </section>
      </main>
    </div>
  );
}
