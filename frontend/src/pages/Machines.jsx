import React, { useReducer, useState } from 'react'

import Sidebar from '../partials/Sidebar'
import Header from '../partials/Header'
import SeeMachinesCard from '../partials/dashboard/SeeMachines'
import RunMachinesCard from '../partials/dashboard/RunMachine'

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
              {/* Cards */}
              <div className="grid w-1/2">
                {/* Bar chart (Direct vs Indirect) */}
                <SeeMachinesCard />
              </div>
            </div>
            <div className="px-4 sm:px-6 lg:px-8 py-8 w-full max-w-9xl mx-auto">
              {/* Cards */}
              <div className="grid w-1/2">
                {/* Bar chart (Direct vs Indirect) */}
                <RunMachinesCard />
              </div>
            </div>
          </main>
        </div>
      </div>
    </filterContext.Provider>
  )
}

export default Dashboard
