import { Link } from 'react-router';
import logo from '../welcome/logo.png';
import './profile_match.css';

export function Profile_Match() {
  return (
    <html lang="en">
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
        <section className="profile-section">
          <div className="profile-box">
            <h2>
              Your Profile <i className="fas fa-pen-square"></i>
            </h2>
          </div>
          <div className="profile-image"></div>
          <input className="inbox" type="text" placeholder="Name:" />
          <input className="inbox" type="text" placeholder="Major:" />
          <input className="inbox" type="text" placeholder="Year:" />

          <div className="input-with-icon">
            <input type="text" placeholder="Can tutor in..." />
            <i className="fas fa-search"></i>
          </div>

          <div className="input-with-icon">
            <input type="text" placeholder="Needs help in..." />
            <i className="fas fa-search"></i>
          </div>

          <div className="toggle">
            <label>
              <b>List me as a one-sided tutor</b>
            </label>
            <input type="checkbox" />
          </div>

          <button className="find-btn">Find Matches!</button>
        </section>

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
    </html>
  );
}
