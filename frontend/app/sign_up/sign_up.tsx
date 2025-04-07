import './sign_up.css';
import logo from '../welcome/logo.png';
import { Link } from 'react-router';

export default function Signup() {
  return (
    <body className="bg-gray-100">
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
          <a href="#" id="link" className="text-gray-700 mr-4 ">
            Sign Up
          </a>
          <Link
            to="/login"
            id="login_button"
            className="text-black px-4 py-2 rounded-lg"
          >
            Login
          </Link>
        </div>
      </nav>

      <div className="bg-gray-100 flex justify-center items-center h-screen">
        <div className="bg-white shadow-lg rounded-lg p-8 w-96">
          <h2 className="text-2xl font-bold text-center mb-2">Sign Up</h2>
          <p className="text-gray-500 text-center mb-6">
            Create an account to unlock exclusive features.
          </p>

          <form>
            <label className="block mb-2 text-gray-700">
              <b>Full Name</b>
            </label>
            <input
              type="name"
              placeholder="Enter your Name"
              className="bg-gray-100 w-full px-3 py-2 rounded-lg focus:outline-none focus:ring-2 mb-4"
            />

            <label className="block mb-2 text-gray-700">
              <b>Email</b>
            </label>
            <input
              type="email"
              placeholder="Enter your Email"
              className="bg-gray-100 w-full px-3 py-2 rounded-lg focus:outline-none focus:ring-2"
            />

            <label className="block mb-2 text-gray-700">
              <b>Password</b>
            </label>
            <input
              type="password"
              placeholder="Enter your Password"
              className="bg-gray-100 w-full px-3 py-2 rounded-lg focus:outline-none focus:ring-2"
            />

            <label className="block mb-2 text-gray-700">
              <b>Re-Enter Password</b>
            </label>
            <input
              type="password"
              placeholder="Re-Enter your Password"
              className="bg-gray-100 w-full px-3 py-2 rounded-lg focus:outline-none focus:ring-2"
            />

            <div className="flex justify-between items-center mt-3">
              <div>
                <input
                  type="checkbox"
                  id="remember-me"
                  className="mr-1"
                ></input>
                <label
                  id="link"
                  htmlFor="remember-me"
                  className="text-gray-600 text-sm"
                >
                  I agree with our Terms and Privacy Policy
                </label>
              </div>
            </div>

            <button
              id="signup_button"
              className="w-full mt-4 bg-blue-500 text-black py-2 rounded-lg hover:bg-primary"
            >
              Sign Up
            </button>

            <div className="text-center my-4 text-gray-500">OR</div>

            <button className="w-full flex items-center justify-center border py-2 rounded-lg hover:bg-gray-100 text-black">
              <img
                src="https://upload.wikimedia.org/wikipedia/commons/thumb/c/c1/Google_%22G%22_logo.svg/512px-Google_%22G%22_logo.svg.png"
                alt="Google Logo"
                className="w-5 h-5 mr-2"
              />
              Login with Google
            </button>

            <p className="text-center text-sm text-gray-600 mt-4">
              Already have an account?{' '}
              <Link to="/login" id="link" className=" hover:underline">
                Login
              </Link>
            </p>
          </form>
        </div>
      </div>
    </body>
  );
}
