import React, { useContext, useState, useRef, useEffect } from 'react'
import Transition from '../../utils/Transition'
import { filterContext } from '../../helpers/Context'

function FilterButton() {
  const { filterContextValue, dispatchFilterContextValue } = useContext(
    filterContext,
  )

  const [dropdownOpen, setDropdownOpen] = useState(false)
  const [checkedBoxes, setCheckedBoxes] = useState([])

  const trigger = useRef(null)
  const dropdown = useRef(null)

  // close on click outside
  useEffect(() => {
    const clickHandler = ({ target }) => {
      if (
        !dropdownOpen ||
        dropdown.current.contains(target) ||
        trigger.current.contains(target)
      )
        return
      setDropdownOpen(false)
    }
    document.addEventListener('click', clickHandler)
    return () => document.removeEventListener('click', clickHandler)
  })

  // close if the esc key is pressed
  useEffect(() => {
    const keyHandler = ({ keyCode }) => {
      if (!dropdownOpen || keyCode !== 27) return
      setDropdownOpen(false)
    }
    document.addEventListener('keydown', keyHandler)
    return () => document.removeEventListener('keydown', keyHandler)
  })

  useEffect(() => {
    filterContextValue.filters
      ? setCheckedBoxes(filterContextValue.filters)
      : setCheckedBoxes(new Array(filterContextValue.labels.length).fill(true))
  }, [filterContextValue])

  const onCheckBox = (e) => {
    const temp = structuredClone(checkedBoxes)
    temp[e.target.name] = !checkedBoxes[e.target.name]
    setCheckedBoxes(temp)
  }

  const applyFilters = () => {
    setDropdownOpen(false)
    dispatchFilterContextValue({
      type: 'setFilters',
      payload: checkedBoxes,
    })
  }

  return (
    <div className="relative inline-flex">
      <button
        ref={trigger}
        className="btn bg-white border-slate-200 hover:border-slate-300 text-slate-500 hover:text-slate-600"
        aria-haspopup="true"
        onClick={() => setDropdownOpen(!dropdownOpen)}
        aria-expanded={dropdownOpen}
      >
        <span className="sr-only">Filter</span>
        <wbr />
        <svg className="w-4 h-4 fill-current" viewBox="0 0 16 16">
          <path d="M9 15H7a1 1 0 010-2h2a1 1 0 010 2zM11 11H5a1 1 0 010-2h6a1 1 0 010 2zM13 7H3a1 1 0 010-2h10a1 1 0 010 2zM15 3H1a1 1 0 010-2h14a1 1 0 010 2z" />
        </svg>
      </button>
      <Transition
        show={dropdownOpen}
        tag="div"
        className="origin-top-right z-10 absolute top-full left-0 right-auto md:left-auto md:right-0 min-w-56 bg-white border border-slate-200 pt-1.5 rounded shadow-lg overflow-hidden mt-1"
        enter="transition ease-out duration-200 transform"
        enterStart="opacity-0 -translate-y-2"
        enterEnd="opacity-100 translate-y-0"
        leave="transition ease-out duration-200"
        leaveStart="opacity-100"
        leaveEnd="opacity-0"
      >
        <div ref={dropdown}>
          <div className="text-xs font-semibold text-slate-400 uppercase pt-1.5 pb-2 px-4">
            Filters
          </div>
          <ul className="mb-4">
            <li className="py-1 px-3">
              {filterContextValue.labels != null ? (
                filterContextValue.labels.map((value, key) => (
                  <label
                    className="flex items-center"
                    key={'Filter-dropdown-' + key}
                  >
                    <input
                      type="checkbox"
                      className="form-checkbox"
                      onChange={onCheckBox}
                      defaultChecked
                      value={checkedBoxes[key]}
                      name={key}
                    />
                    <span className="text-sm font-medium ml-2">{value}</span>
                  </label>
                ))
              ) : (
                <></>
              )}
            </li>
          </ul>
          <div className="py-2 px-3 border-t border-slate-200 bg-slate-50">
            <ul className="flex items-center justify-between">
              <li>
                <button
                  className="btn-xs bg-indigo-500 hover:bg-indigo-600 text-white"
                  onClick={applyFilters}
                  onBlur={() => setDropdownOpen(false)}
                >
                  Apply
                </button>
              </li>
            </ul>
          </div>
        </div>
      </Transition>
    </div>
  )
}

export default FilterButton
