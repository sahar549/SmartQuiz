import React from 'react'

const Header = ({isQuizDisplayed}) => {
  return (
    <header className='text-3xl -mb-4 center justify-between items-center p-4 bg-white text-black'>
      <div className='logo '>
        <h1 className=' text-xxxl font-medium text-black '>SMART-Quiz </h1>
        {!isQuizDisplayed && (
        <p className='text-slate-400'> Welcome To Ai-Quiz generator </p>    
        )}
      </div>
      
    </header>
  )
}

export default Header
