/**
 * Created by Manuel on 13/03/2017.
 */

export class Property {

    constructor(name, location){
        this.name = name;
        this.location = location;
    }

    getName(){
       return this.name;
    }

    getLocation(){
        return this.location;
    }

    evaluate(memoryState = {}){
        let value = memoryState.getValue(this.getName()) || undefined;
        return eval(value);
    }
}