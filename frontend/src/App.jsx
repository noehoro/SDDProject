import React, { useEffect, useReducer } from 'react'
import { useLocation, Routes, Route } from 'react-router-dom'

import './css/style.css'

import './charts/ChartjsConfig'

import { contextReducer } from './helpers/reducers'
import { Context } from './helpers/Context'

import { PrivateRoute } from './helpers/Routes'

// Import pages
import Dashboard from './pages/Dashboard'
import Login from './pages/Login'

const App = () => {
  const [contextValue, dispatchContextValue] = useReducer(contextReducer, {
    loggedIn: localStorage.getItem('loggedIn')
      ? localStorage.getItem('loggedIn')
      : false,
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
        <Route exact path="/login" element={<Login />} />
      </Routes>
    </Context.Provider>
  )
}

export default App
