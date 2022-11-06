import React, { useContext, useEffect, useState } from 'react'
import { filterContext } from '../../helpers/Context'

// Import utilities
import { tailwindConfig } from '../../utils/Utils'

const RunMachinesCard = () => {
  const { dispatchFilterContextValue } = useContext(filterContext)

  const [inputs, setInputs] = useState({
    machineID: '',
  })

  const handleInputChange = (e) => {
    const value = e.target.value
    setInputs({
      ...inputs,
      [e.target.id]: value,
    })
  }

  const handleMachineRun = () => {}

  return (
    <div className="flex w-4/5 flex-col col-span-full sm:col-span-6 bg-white shadow-lg rounded-sm border border-slate-200">
      <header className="px-5 py-4 border-b border-slate-100">
        <h2 className="font-semibold text-slate-800">Run Machines</h2>
      </header>
      <div className="p-4 w-3/5">
        <br />
        <div className="mb-4">
          <label className="block text-sm font-medium mb-1" htmlFor="machineID">
            Machine ID
          </label>
          <input
            id="machineID"
            className="form-input w-full"
            value={inputs.machineID}
            type="number"
            onChange={handleInputChange}
          />
        </div>

        <button
          className="btn bg-indigo-500 hover:bg-indigo-600 text-white"
          onClick={handleMachineRun}
        >
          Run Machine
        </button>
      </div>
    </div>
  )
}

export default RunMachinesCard
