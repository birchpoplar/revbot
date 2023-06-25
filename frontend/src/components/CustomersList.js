import React, { useState } from 'react';
import axios from 'axios';

const CustomersList = () => {
  const [customers, setCustomers] = useState(null);

  const fetchData = async () => {
    try {
      const response = await axios.get('/customers');
      setCustomers(response.data.data);
    } catch (err) {
      console.error(err);
    }
  };
  
  return (
    <div>
      <button onClick={fetchData}>Fetch Customers</button>

      {customers && (
        <ul style={{listStyleType: 'none', padding: 0}}>
          {customers.map((customer, index) => (
            <li key={index} style={{border: '1px solid #000', margin: '10px 0', padding: '10px'}}>
              {customer.name}
            </li>
          ))}
        </ul>
      )}
    </div>
  );

};

export default CustomersList;