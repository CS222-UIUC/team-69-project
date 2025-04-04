import logo from './logo.png';
import '../login.css';

export function Welcome() {
  return (
    <body className="bg-gray-100">
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
          <a href="#" id="link" className="text-gray-700 mr-4 ">
            Sign Up
          </a>
          <a
            href="#"
            id="login_button"
            className="text-black px-4 py-2 rounded-lg"
          >
            Login
          </a>
        </div>
      </nav>

      <div className="flex justify-center items-center h-screen">
        <div className="bg-white shadow-lg rounded-lg p-8 w-96">
          <h2 className="text-2xl font-bold text-center mb-2">Login</h2>
          <p className="text-gray-500 text-center mb-6">
            Welcome back! Please log in to access your account.
          </p>

          <form>
            <label className="block mb-2 text-gray-700">Email</label>
            <input
              type="email"
              placeholder="Enter your Email"
              className="w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-400 mb-4"
            />

            <label className="block mb-2 text-gray-700">Password</label>
            <input
              type="password"
              placeholder="Enter your Password"
              className="w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-400"
            />

            <div className="flex justify-between items-center mt-3">
              <div>
                <input
                  type="checkbox"
                  id="remember-me"
                  className="mr-1"
                ></input>
                <label htmlFor="remember-me" className="text-gray-600 text-sm">
                  Remember Me
                </label>
              </div>
              <a
                href="#"
                id="link"
                className="text-sm text-gray-600 hover:underline"
              >
                Forgot Password?
              </a>
            </div>

            <button
              id="login_button"
              className="w-full mt-4 bg-blue-500 text-black py-2 rounded-lg hover:bg-primary"
            >
              Login
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
              Don't have an account?{' '}
              <a href="#" id="link" className=" hover:underline">
                Sign Up
              </a>
            </p>
          </form>
        </div>
      </div>

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
    </body>
  );
}
