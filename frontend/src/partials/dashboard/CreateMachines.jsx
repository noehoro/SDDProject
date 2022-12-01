import React, { useContext, useEffect, useState } from 'react'
import { newMachineCall } from '../../helpers/apiCalls'
import { filterContext } from '../../helpers/Context'

// Import utilities
import { tailwindConfig } from '../../utils/Utils'

const BarGraphCard = () => {
  const { dispatchFilterContextValue } = useContext(filterContext)
  const [imageURL, setImageURL] = useState('')

  const [inputs, setInputs] = useState({
    name: '',
    duration: '',
  })

  const handleInputChange = (e) => {
    const value = e.target.value
    setInputs({
      ...inputs,
      [e.target.id]: value,
    })
  }

  const handleCreate = async () => {
    const url = await newMachineCall(inputs)
    setImageURL(url)
  }

  return (
    <div className="flex w-4/5 flex-col col-span-full sm:col-span-6 bg-white shadow-lg rounded-sm border border-slate-200">
      <header className="px-5 py-4 border-b border-slate-100">
        <h2 className="font-semibold text-slate-800">Admin Dashboard</h2>
      </header>
      <div className="p-4 w-3/5">
        <h1>Create Machine</h1>
        <br />
        <div className="mb-4">
          <label className="block text-sm font-medium mb-1" htmlFor="name">
            Name
          </label>
          <input
            id="name"
            className="form-input w-full"
            value={inputs.name}
            type="text"
            onChange={handleInputChange}
          />
        </div>
        <div className="mb-4">
          <label className="block text-sm font-medium mb-1" htmlFor="duration">
            Duration in Minutes
          </label>
          <input
            id="duration"
            className="form-input w-full"
            value={inputs.duration}
            type="number"
            onChange={handleInputChange}
          />
        </div>

        <button
          className="btn bg-indigo-500 hover:bg-indigo-600 text-white"
          onClick={handleCreate}
        >
          Create Machine
        </button>
      </div>
      {imageURL && (
        <div className="p-4 w-3/5">
          <h1>New Machine QR Code</h1>
          <br />
          <img src={imageURL} alt="" />
        </div>
      )}
    </div>
  )
}

export default BarGraphCard
