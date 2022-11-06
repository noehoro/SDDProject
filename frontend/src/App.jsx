import React, { useEffect, useReducer } from 'react'
import { useLocation, Routes, Route } from 'react-router-dom'

import './css/style.css'

import { contextReducer } from './helpers/reducers'
import { Context } from './helpers/Context'

import { PrivateRoute } from './helpers/Routes'

// Import pages
import Dashboard from './pages/Dashboard'
import Machines from './pages/Machines'
import Login from './pages/Login'

const App = () => {
  const [contextValue, dispatchContextValue] = useReducer(contextReducer, {
    loggedIn: true,
    username: localStorage.getItem('username')
      ? localStorage.getItem('username')
      : '',
  })

  const location = useLocation()

  useEffect(() => {
    document.querySelector('html').style.scrollBehavior = 'auto'
    window.scroll({ top: 0 })
    document.querySelector('html').style.scrollBehavior = ''
  }, [location.pathname]) // triggered on route change

  return (
    <Context.Provider value={{ contextValue, dispatchContextValue }}>
      <Routes>
        <Route
          exact
          path="/"
          element={<PrivateRoute element={<Dashboard />}></PrivateRoute>}
        />
        <Route
          exact
          path="/machines"
          element={<PrivateRoute element={<Machines />}></PrivateRoute>}
        />
        <Route exact path="/login" element={<Login />} />
      </Routes>
    </Context.Provider>
  )
}

export default App
