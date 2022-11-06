import React, { useContext, useEffect, useState } from 'react'
import { filterContext } from '../../helpers/Context'

// Import utilities
import { tailwindConfig } from '../../utils/Utils'

const SeeMachinesCard = () => {
  const { dispatchFilterContextValue } = useContext(filterContext)

  const [machineNames, setMachineNames] = useState([])
  const [machineTimes, setMachineTimes] = useState([])

  useEffect(() => {
    const names = ['machine 1', 'machine 2']
    const times = [20, 40]
    setMachineNames(names)
    setMachineTimes(times)
  }, [])

  const getPercentage = (key) => {
    return Math.round((machineTimes[key] / 60) * 100)
  }

  return (
    <div className="flex w-4/5 flex-col col-span-full sm:col-span-6 bg-white shadow-lg rounded-sm border border-slate-200">
      <header className="px-5 py-4 border-b border-slate-100">
        <h2 className="font-semibold text-slate-800">Machines</h2>
      </header>
      <br />
      <div className="p-4 w-3/5">
        {machineNames.map((value, key) => (
          <div className="mb-4">
            <h1 className="mb-4">{value}</h1>
            <div className="w-full bg-gray-200 rounded-full dark:bg-gray-700">
              <div
                className="bg-blue-600 text-xs font-medium text-blue-100 text-center p-0.5 leading-none rounded-full"
                style={{ width: `${getPercentage(key)}%` }}
              ></div>
              {machineTimes[key]}/60 mins
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}

export default SeeMachinesCard
