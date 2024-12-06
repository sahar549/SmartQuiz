import React from 'react';

const GenerateButton = ({ onClick }) => {
  return (
    <button 
      onClick={onClick} 
      className="mt-4 bg-gray-600 text-white py-2 px-10 rounded hover:bg-fuchsia-600 transition duration-200"
    >
      Generate quiz
    </button>
  );
};

export default GenerateButton;
