async function getHistoricOnline () {
    try{
            const response = await fetch('api/dashboard/connectUser/', {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json',
                }
            });

            if (!response.ok) {
                throw new Error('La requête a échoué avec le code : ' + response.status);
            }
    
            console.log(response)
            const data = await response.json();
            console.log("data :", data)
    
    }catch (error){
        console.error("Erreur :", error.message)
    }
}