import "css-doodle"
import * as React from "react";

export function BackgroundDoodle({ style }: { style?: React.CSSProperties }) {

    const Doodle = 'css-doodle' as any
    return (
        <div style={{
            width: "100%",
            height: "100%",
            ...style,
        }}>
            <Doodle>
                {`
                    :doodle{
                        @grid: 50 / 100% / transparent;
                      }

                    @size: 4vw;
                    background:#23A523FF;
                    @shape: clover 4;

                    transform: scale(@rand(0.4, 0.9));
                    transition: .3s cubic-bezier(.175, .885, .32, 1.275);
                    transition-delay: @rand(100ms);

                    animation: breath 2s ease-in-out infinite;
                    animation-delay: @rand(1s, 2s);
                    @keyframes breath {
                        0%, 100% { opacity: 1; }
                        50% { opacity: 0.5; }
                    }
                `}
            </Doodle>
        </div>
    )
}

function BackgroundCard(){

    const Doodle = 'css-doodle' as any  //使用断言阻止类型错误
    return (
        <div style={{
            width: "100%",
            height:"200px"
        }}>
            <Doodle>
                {`
                    :doodle{
                        @grid: 50 / 100% / #202020;
                      }
                    
                    @size: 4vw;
                    background:#23A523FF;
                    @shape: clover 4;
                    
                    transform: scale(@rand(0.4, 0.9));
                    transition: .3s cubic-bezier(.175, .885, .32, 1.275);
                    transition-delay: @rand(100ms);
                    
                    animation: breath 2s ease-in-out infinite;
                    animation-delay: @rand(1s, 2s);
                    @keyframes breath {
                        0%, 100% { opacity: 1; }
                        50% { opacity: 0.5; }
                    }
                `}
            </Doodle>


        </div>
    )
}

export default function Background(){

    return(
        <>
            <div style={{backgroundColor:"beige", height:"100vh",width:"100%",padding:"0px"}} >
                <div style={{backgroundColor:"rgb(0,0,0,10%)", height:"100%",width:"100%",padding:"0px"}} >
                    <BackgroundCard/>
                </div>
            </div>
        </>
        )
}
