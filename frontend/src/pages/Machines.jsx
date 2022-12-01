import React, { useReducer, useState } from 'react'

import Sidebar from '../partials/Sidebar'
import Header from '../partials/Header'
import SeeMachinesCard from '../partials/dashboard/SeeMachines'
import RunMachinesCard from '../partials/dashboard/RunMachine'

function Dashboard() {
  const [sidebarOpen, setSidebarOpen] = useState(false)
  const [machine, setMachine] = useState(false)
  return (
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
              <SeeMachinesCard machine={machine} />
            </div>
          </div>
          <div className="px-4 sm:px-6 lg:px-8 py-8 w-full max-w-9xl mx-auto">
            {/* Cards */}
            <div className="grid w-1/2">
              {/* Bar chart (Direct vs Indirect) */}
              <RunMachinesCard machine={setMachine} />
            </div>
          </div>
        </main>
      </div>
    </div>
  )
}

export default Dashboard
