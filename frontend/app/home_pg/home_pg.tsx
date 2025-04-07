import { Link } from "react-router"
import "./home_pg.css"
import logo from '../welcome/logo.png';
import hero_img from "./hero_img.png";
import how_it_works from "./how_it_works.png"

export function Home_Pg() {
    return (
        <html lang="en">
            <body>
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
                <button className="btn"><Link to="/">Join Today!</Link></button>
            </section>

            <section className="section how-it-works">
                <div className="flex justify-center items-center">
                    <img src={how_it_works} alt="How It Works" />
                    <a href="link1.html" className="arrow-link arrow1" aria-label="Go to step 1"></a>
                    <a href="link2.html" className="arrow-link arrow2" aria-label="Go to step 2"></a>
                    <a href="link3.html" className="arrow-link arrow3" aria-label="Go to step 3"></a>
                </div>
            </section>

            <section className="section sneak-peek">
                <h2>A Sneak Peek at our Top Profiles!</h2>
                <div className="profiles">
                <div className="profile-card">
                    <h4>A. R.</h4>
                    <p><b>Can Tutor In:</b> CS101, CS201<br/><b>Major:</b> Comp Sci<br/><b>Rating:</b> ⭐⭐⭐⭐⭐</p>
                </div>
                <div className="profile-card">
                    <h4>C. A.</h4>
                    <p><b>Can Tutor In:</b> STAT200, MATH220<br/><b>Major:</b> Stats<br/><b>Rating:</b> ⭐⭐⭐⭐</p>
                </div>
                <div className="profile-card">
                    <h4>Y. O.</h4>
                    <p><b>Can Tutor In:</b> PHYS211<br/><b>Major:</b> Physics<br/><b>Rating:</b> ⭐⭐⭐⭐⭐</p>
                </div>
                <div className="profile-card">
                    <h4>A. U.</h4>
                    <p><b>Can Tutor In:</b> ANTH101<br/><b>Major:</b> Anthro<br/><b>Rating:</b> ⭐⭐⭐⭐</p>
                </div>
                <div className="profile-card">
                    <h4>E. B.</h4>
                    <p><b>Can Tutor In:</b> MATH140<br/><b>Major:</b> Math<br/><b>Rating:</b> ⭐⭐⭐⭐⭐</p>
                </div>
                <div className="profile-card">
                    <h4>A. B. S.</h4>
                    <p><b>Can Tutor In:</b> CHEM101<br/><b>Major:</b> Chem<br/><b>Rating:</b> ⭐⭐⭐⭐</p>
                </div>
                </div>
            </section>
            </body>
        </html>
    )
}