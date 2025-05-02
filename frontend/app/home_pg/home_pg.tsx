import { Link, useNavigate } from 'react-router';
import './home_pg.css';
import logo from '../assets/logo.png';
import hero_img from './hero_img.png';
import how_it_works from './how_it_works.png';
import { useEffect } from 'react';

export function Home_Pg() {
  const navigate = useNavigate();

  useEffect(() => {
    const check_auth = async () => {
      const response = await fetch(
        `${import.meta.env.VITE_API_BASE}/user/@me`,
        {
          credentials: 'include',
        }
      );
      if (response.status == 200) {
        navigate('/matches');
      }
    };
    check_auth();
  }, []);

  return (
    <div className="homepage">
      <div>
        <nav className="flex justify-between items-center px-8 py-4 bg-white shadow-md">
          <img src={logo} className="w-32" />
          <ul className="flex space-x-6 text-gray-700">
            <li>
              <Link to="/" id="link">
                Home
              </Link>
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
          <div>
            <Link to="/signup" id="link" className="text-gray-700 mr-4 ">
              Sign Up
            </Link>
            <Link
              to="/login"
              id="login_button"
              className="text-black px-4 py-2 rounded-lg"
            >
              Login
            </Link>
          </div>
        </nav>

        <section className="hero">
          <div className="flex justify-center items-center">
            <img src={hero_img} alt="Hero Illustration" />
          </div>
          <h1>Find a Tutor. Be a Tutor.</h1>
          <button className="btn">
            <Link to="/signup">Join Today!</Link>
          </button>
        </section>

        <section className="section how-it-works">
          <div className="flex justify-center items-center">
            <img src={how_it_works} alt="How It Works" />
            <a
              href="#"
              className="arrow-link arrow1"
              aria-label="Go to step 1"
            ></a>
            <a
              href="#"
              className="arrow-link arrow2"
              aria-label="Go to step 2"
            ></a>
            <a
              href="#"
              className="arrow-link arrow3"
              aria-label="Go to step 3"
            ></a>
          </div>
        </section>

        <section className="section sneak-peek">
          <h2>A Sneak Peek at our Top Profiles!</h2>
          <div className="profiles">
            <div className="profile-card">
              <div className="circle"></div>
              <h4>
                <b>A. R.</b>
              </h4>
              <div>
                <b>Can Tutor In:</b> CS101, CS201
                <br />
                <b>Major:</b> Comp Sci
                <br />
                <b>Rating:</b> <p>⭐⭐⭐⭐⭐</p>
              </div>
            </div>
            <div className="profile-card">
              <div className="circle"></div>
              <h4>
                <b>C. A.</b>
              </h4>
              <div>
                <b>Can Tutor In:</b> STAT200, MATH220
                <br />
                <b>Major:</b> Stats
                <br />
                <b>Rating:</b> <p>⭐⭐⭐⭐</p>
              </div>
            </div>
            <div className="profile-card">
              <div className="circle"></div>
              <h4>
                <b>Y. O.</b>
              </h4>
              <div>
                <b>Can Tutor In:</b> PHYS211
                <br />
                <b>Major:</b> Physics
                <br />
                <b>Rating:</b> <p>⭐⭐⭐⭐⭐</p>
              </div>
            </div>
            <div className="profile-card">
              <div className="circle"></div>
              <h4>
                <b>A. U.</b>
              </h4>
              <div>
                <b>Can Tutor In:</b> ANTH101
                <br />
                <b>Major:</b> Anthro
                <br />
                <b>Rating:</b> <p>⭐⭐⭐⭐</p>
              </div>
            </div>
            <div className="profile-card">
              <div className="circle"></div>
              <h4>
                <b>E. B.</b>
              </h4>
              <div>
                <b>Can Tutor In:</b> MATH140
                <br />
                <b>Major:</b> Math
                <br />
                <b>Rating:</b> <p>⭐⭐⭐⭐⭐</p>
              </div>
            </div>
            <div className="profile-card">
              <div className="circle"></div>
              <h4>
                <b>A. B. S.</b>
              </h4>
              <div>
                <b>Can Tutor In:</b> CHEM101
                <br />
                <b>Major:</b> Chem
                <br />
                <b>Rating:</b> <p>⭐⭐⭐⭐</p>
              </div>
            </div>
          </div>
        </section>
        <section className="section search-section">
          <h1>Find a Tutor For</h1>
          <div className="search-bar">
            <input type="text" placeholder="What would you like to learn?" />
            <button type="submit">
              <i className="fas fa-search"></i>
            </button>
          </div>
        </section>
        <footer className="bg-gray-100 py-6 text-center text-gray-600 text-sm">
          <div className="mt-2 flex justify-center space-x-4">
            <a href="#" className="hover:text-blue-500">
              Facebook
            </a>
            <a href="#" className="hover:text-blue-500">
              Twitter
            </a>
            <a href="#" className="hover:text-blue-500">
              LinkedIn
            </a>
          </div>
        </footer>
      </div>
    </div>
  );
}
