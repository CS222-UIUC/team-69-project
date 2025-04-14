import './sign_up.css';
import logo from '../assets/logo.png';
import { z } from 'zod';
import { useNavigate } from 'react-router';

const signupSchema = z.object({
  display_name: z.string(),
  email: z.string().max(255),
  password: z.string().max(72),
});

export function Signup() {
  const navigate = useNavigate();

  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();

    const formData = new FormData(e.currentTarget);
    const data = Object.fromEntries(formData);

    const { success, data: verifiedData } = signupSchema.safeParse(data);
    if (!success) {
      return alert('Signup information is incorrect.');
    }

    if (!verifiedData.email.endsWith('@illinois.edu')) {
      return alert('You must use an illinois.edu email to signup');
    }

    const response = await fetch(`${import.meta.env.VITE_API_BASE}/signup`, {
      method: 'POST',
      body: JSON.stringify(verifiedData),
      headers: {
        'Content-Type': 'application/json',
      },
    });
    if (response.status !== 200) {
      return alert('Failed to signup.');
    }
    console.log(await response.json());

    navigate('/');
  };

  return (
    <div className="bg-gray-100">
      <nav className="flex justify-between items-center px-8 py-4 bg-white shadow-md">
        <img src={logo} className="w-32" />
        <ul className="flex space-x-6 text-gray-700 -ml-50">
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
          <h2 className="text-2xl font-bold text-center mb-2 text-gray-500">
            Sign Up
          </h2>
          <p className="text-gray-500 text-center mb-6">
            Create an account to unlock exclusive features.
          </p>

          <form className="text-black" onSubmit={handleSubmit}>
            <label className="block mb-2 text-gray-700">
              <b>Full Name</b>
            </label>
            <input
              type="name"
              placeholder="Enter your Name"
              name="display_name"
              className="bg-gray-100 w-full px-3 py-2 rounded-lg focus:outline-none focus:ring-2 mb-"
            />

            <label className="block mb-2 text-gray-700">
              <b>Email</b>
            </label>
            <input
              type="email"
              name="email"
              placeholder="Enter your Email"
              className="bg-gray-100 w-full px-3 py-2 rounded-lg focus:outline-none focus:ring-2"
            />

            <label className="block mb-2 text-gray-700">
              <b>Password</b>
            </label>
            <input
              type="password"
              name="password"
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

              type="submit"

              className="w-full mt-4 bg-blue-500 text-black py-2 rounded-lg hover:bg-primary"
            >
              Sign Up
            </button>

            <div className="text-center my-4 text-gray-500">OR</div>

            <button
              id="google_button"
              className="bg-gray-100 w-full flex items-center justify-center py-2 rounded-lg hover:bg-gray-100"
            >
              <img
                src="https://upload.wikimedia.org/wikipedia/commons/thumb/5/53/Google_%22G%22_Logo.svg/512px-Google_%22G%22_Logo.svg.png"
                alt="Google Logo"
                className="w-5 h-5 mr-2"
              />
              Sign Up with Google
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
    </div>
  );
}
