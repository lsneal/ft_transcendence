import AbstractView from "./AbstractView.js";

export default class extends AbstractView {
    constructor(params) {
        super(params);
        this.setTitle("Login42");
   
    }

    async executeViewScript()
    {
      async function EventLogin42Get () {
        const params = new URLSearchParams(location.search);
        const code = params.get('code')
        console.log(code)

        try {
            const response = fetch('/api/users/login42/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    code: code,
                })
            }).then((response) => {
              window.history.pushState(null, "Profile", "/profile/");
              window.dispatchEvent(new Event('popstate'));
            });
            
        }
        catch (error) {
          console.log(error);
        };
      }
      EventLogin42Get();

    }


    async getHtml() {
      try{
        const response = await fetch('/home.html');
        if (!response.ok){
            throw new Error('Failed to fetch Home.html');
        }
        const html = await response.text();
        return html;
      } catch(error){
        console.error('Error fetchin', error);
        return '<p>Error loading </p>'
      }
    }
}