import React, { useContext } from 'react'
import { Navigate } from 'react-router-dom'
import { Context } from './Context'

export const PrivateRoute = ({ element }) => {
  const { contextValue } = useContext(Context)
  if (!contextValue || !contextValue.loggedIn) {
    return <Navigate to="/login" />
  }
  return element
}
