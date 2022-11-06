import React, { useContext, useState } from 'react'
import { Link } from 'react-router-dom'

import LogoImage from '../images/login_background.jpg'
import AuthDecoration from '../images/auth-decoration.png'
import logo from '../images/logo.png'
import { logInCall } from '../helpers/apiCalls'
import { Context } from '../helpers/Context'

const Login = () => {
  const { contextValue, dispatchContextValue } = useContext(Context)

  const [status, setStatus] = useState('')
  const [inputs, setInputs] = useState({
    username: '',
    password: '',
  })

  const handleInputChange = (e) => {
    const value = e.target.value
    setInputs({
      ...inputs,
      [e.target.id]: value,
    })
  }

  const handleLogin = async () => {
    if (!inputs.username || !inputs.password) {
      setStatus('Missing Parameter')
      return
    }
    const res = await logInCall(inputs)
    console.log(res)
    if (res) {
      setStatus('')
      dispatchContextValue({
        type: 'login',
        payload: inputs.username,
      })
    } else {
      setStatus('Wrong Username or Password')
    }
  }
  return (
    <main className="bg-white">
      <div className="relative md:flex">
        {/* Content */}
        <div className="md:w-1/2">
          <div className="min-h-screen h-full flex flex-col after:flex-1">
            {/* Header */}
            <div className="flex-1">
              <div className="flex justify-center px-4 sm:px-6 lg:px-8">
                {/* Logo */}
                <Link className="" to="/">
                  <img src={logo} alt="" />
                </Link>
              </div>
            </div>

            <div className="max-w-sm mx-auto px-4 py-8">
              {/* Form */}
              {contextValue.loggedIn ? (
                <>
                  <h5 className="text-3xl text-slate-800 font-bold mb-6">
                    Welcome back {contextValue.username}! ✨
                  </h5>
                  <Link
                    className="btn bg-indigo-500 hover:bg-indigo-600 text-white ml-3"
                    to="/"
                  >
                    Dashboard
                  </Link>
                </>
              ) : (
                <>
                  <h1 className="text-3xl text-slate-800 font-bold mb-6">
                    Welcome back! ✨
                  </h1>
                  <div className="space-y-4">
                    <div>
                      <label
                        className="block text-sm font-medium mb-1"
                        htmlFor="username"
                      >
                        Username
                      </label>
                      <input
                        id="username"
                        className="form-input w-full"
                        value={inputs.username}
                        type="username"
                        onChange={handleInputChange}
                      />
                    </div>
                    <div>
                      <label
                        className="block text-sm font-medium mb-1"
                        htmlFor="password"
                      >
                        Password
                      </label>
                      <input
                        id="password"
                        className="form-input w-full"
                        value={inputs.password}
                        type="password"
                        autoComplete="on"
                        onChange={handleInputChange}
                      />
                    </div>
                  </div>
                  <div className="flex items-center justify-between mt-6">
                    <div className="mr-1">
                      <Link
                        className="text-sm underline hover:no-underline"
                        to="/reset-password"
                      >
                        Forgot Password?
                      </Link>
                    </div>
                    <button
                      className="btn bg-indigo-500 hover:bg-indigo-600 text-white ml-3"
                      onClick={handleLogin}
                    >
                      Sign In
                    </button>
                  </div>
                </>
              )}

              {/* Warning */}
              {status && (
                <div className="pt-5 mt-6 border-t border-slate-200">
                  <div className="mt-5">
                    <div className="bg-amber-100 text-amber-600 px-3 py-2 rounded">
                      <span className="text-sm">{status}</span>
                    </div>
                  </div>
                </div>
              )}
            </div>
          </div>
        </div>

        {/* Image */}
        <div
          className="hidden md:block absolute top-0 bottom-0 right-0 md:w-1/2"
          aria-hidden="true"
        >
          <img
            className="object-cover object-center w-full h-full"
            src={LogoImage}
            width="760"
            height="1024"
            alt="Authentication"
          />
          <img
            className="absolute top-1/4 left-0 -translate-x-1/2 ml-8 hidden lg:block"
            src={AuthDecoration}
            width="218"
            height="224"
            alt="Authentication decoration"
          />
        </div>
      </div>
    </main>
  )
}

export default Login
