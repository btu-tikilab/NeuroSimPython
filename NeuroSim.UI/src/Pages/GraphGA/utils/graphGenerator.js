export function generateRandomGraph(nodeCount, allowSelfLoop) {

    const nodes = [];
    const edges = [];

    for (let i = 1; i <= nodeCount; i++) {

        nodes.push({
            data:{
                id:String(i),
                label:String(i),
            }
        });

    }

    for (let i = 1; i <= nodeCount; i++) {

        const connections = Math.floor(Math.random()*3)+1;

        for(let j=0;j<connections;j++){

            const target =
                Math.floor(Math.random()*nodeCount)+1;

            if(target===i && !allowSelfLoop)
                continue;

            edges.push({

                data:{
                    id:`${i}-${target}-${j}`,
                    source:String(i),
                    target:String(target)
                }

            });

        }

    }

    return{

        nodes,
        edges,
        elements:[
            ...nodes,
            ...edges
        ]

    };

}