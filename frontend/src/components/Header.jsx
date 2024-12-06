import React from 'react'

const Header = ({isQuizDisplayed}) => {
  return (
    <header className='text-3xl -mb-4 center justify-between items-center p-4  text-black  bg-gradient-to-r from-purple-200 via-purple-200 to-purple-400'>
      <div className='logo '>
        <h1 className=' text-xxl font-medium text-fuchsia-600 '>SMART_Quiz </h1>
        {!isQuizDisplayed && (
        <p className='text-slate-400'> "Ai-Quiz generator" </p>    
        )}
      </div>
      
    </header>
  )
}

export default Header
