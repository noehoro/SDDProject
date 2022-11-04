import React, { useReducer, useState } from 'react'

import Sidebar from '../partials/Sidebar'
import Header from '../partials/Header'
import WelcomeBanner from '../partials/dashboard/WelcomeBanner'
import FilterButton from '../partials/actions/FilterButton'
import Datepicker from '../partials/actions/Datepicker'
import BarGraphCard from '../partials/dashboard/BarGraphCard'

import { filterContextReducer } from '../helpers/reducers'
import { filterContext } from '../helpers/Context'

function Dashboard() {
  const [filterContextValue, dispatchFilterContextValue] = useReducer(
    filterContextReducer,
    {
      filters: null,
      labels: [],
    },
  )

  const [sidebarOpen, setSidebarOpen] = useState(false)

  return (
    <filterContext.Provider
      value={{ filterContextValue, dispatchFilterContextValue }}
    >
      <div className="flex h-screen overflow-hidden">
        {/* Sidebar */}
        <Sidebar sidebarOpen={sidebarOpen} setSidebarOpen={setSidebarOpen} />

        {/* Content area */}
        <div className="relative flex flex-col flex-1 overflow-y-auto overflow-x-hidden">
          {/*  Site header */}
          <Header sidebarOpen={sidebarOpen} setSidebarOpen={setSidebarOpen} />

          <main>
            <div className="px-4 sm:px-6 lg:px-8 py-8 w-full max-w-9xl mx-auto">
              {/* Welcome banner */}
              <WelcomeBanner />

              {/* Dashboard actions */}
              <div className="sm:flex sm:justify-between sm:items-center mb-8">
                {/* Right: Actions */}
                <div></div>
                <div className="grid grid-flow-col sm:auto-cols-max justify-end sm:justify-end gap-2">
                  {/* Filter button */}
                  <FilterButton />
                  {/* Datepicker built with flatpickr */}
                  <Datepicker />
                </div>
              </div>

              {/* Cards */}
              <div className="grid w-full">
                {/* Bar chart (Direct vs Indirect) */}
                <BarGraphCard />
              </div>
            </div>
          </main>
        </div>
      </div>
    </filterContext.Provider>
  )
}

export default Dashboard
