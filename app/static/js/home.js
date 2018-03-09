$(document).ready(function(){
    moment.locale('pt-BR');
    //moment.locale('en-US');

    get_status_charge = function(status) {
        if(status.trim() == '00 No charging') {
            return 'Não carregando'
        } else if(status.trim() == '02 Boost') {
            return 'Carregando'
        } else if(status.trim() == '01 Float') {
            return 'Flutuando'
        }
        return status;
    }
    get_status_battery = function(status) {
        if(status.trim() == '00H Normal') {
            return 'Normal'
        }
        return status;
    }
    get_data = function() {
        $.get(url_context + 'device/monitorredirect', function(datajson) {
            console.log(datajson)
            data = datajson.sample

//            $('#pvvoltage').text(data.pv.voltage)
//            $('#pvcurrent').text(data.pv.current)
//            $('#pvpower').text(data.pv.power)

            //$('#pvvoltagemax').text(data.statistical.VoltageMaxPV)
            //$('#pvvoltagemin').text(data.statistical.VoltageMinPV)

            $('#pvpoweravg').text(datajson.generated.power.avg.toFixed(2))
            $('#pvpowermax').text(datajson.generated.power.max)
            $('#pvpowermin').text(datajson.generated.power.min)
            //$('#pvpowertotal').text(datajson.generated.power.total.toFixed(2))

            $('#pvvoltageavg').text(datajson.generated.voltage.avg.toFixed(2))
            $('#pvvoltagemax').text(datajson.generated.voltage.max)
            $('#pvvoltagemin').text(datajson.generated.voltage.min)

            $('#pvcurrentavg').text(datajson.generated.current.avg.toFixed(2))
            $('#pvcurrentmax').text(datajson.generated.current.max)
            $('#pvcurrentmin').text(datajson.generated.current.min)
            $('#pvcurrenttotal').text(datajson.generated.current.total.toFixed(2))

            //$('#generatedenergy').text(data.statistical.GeneratedEnergy)

//            $('#batteryvoltage').text(data.battery.voltage)
//            $('#batterycurrent').text(data.battery.current)
//            $('#batterypower').text(data.battery.power)

            $('#batterysoc').width( data.BatterySOC +'%');
            $('#batterysocvalue').text(data.BatterySOC + '%')

            $('#batterystatus').text(get_status_battery(data.StatusBattery))
            $('#batterycharge').text(get_status_charge(data.StatusCharge))

            $('#batterytemperature').text(data.temperature.Battery)
            $('#batterytemperatureremote').text(data.temperature.RemoteBattery)

            //$('#batteryvoltagemax').text(data.statistical.VoltageMaxBattery)
            //$('#batteryvoltagemin').text(data.statistical.VoltageMinBattery)

            var toValue = function(value) {
                return !value ? 0 : value.toFixed(2)
            };
            $('#batterypoweravg').text(toValue(datajson.battery.power.avg))
            $('#batterypowermax').text(datajson.battery.power.max)
            $('#batterypowermin').text(datajson.battery.power.min)

            $('#batteryvoltageavg').text(toValue(datajson.battery.voltage.avg))
            $('#batteryvoltagemax').text(datajson.battery.voltage.max)
            $('#batteryvoltagemin').text(datajson.battery.voltage.min)

            $('#batterycurrentavg').text(toValue(datajson.battery.current.avg))
            $('#batterycurrentmax').text(datajson.battery.current.max)
            $('#batterycurrentmin').text(datajson.battery.current.min)

//            $('#dischargingvoltage').text(data.discharging.voltage)
//            $('#dischargingcurrent').text(data.discharging.current)
//            $('#dischargingpower').text(data.discharging.power)
            //$('#consumedenergy').text(data.statistical.ConsumedEnergy)

//            $('#systemvoltage').text(data.VoltageSystemBattery)
//            $('#temperatureinsideequipment').text(data.temperature.InsideEquipment)
//            $('#temperaturepowercomponents').text(data.temperature.PowerComponents)
//            $('#statusdischarging').text(data.StatusDischarging)

            $('#rtc').text(moment(data.CreatedDate).format('LLLL'))
            $('.pvicon').removeClass('fa-sun fa-moon')
            $('#ctn_pv').removeClass('bg-light text-dark bg-dark text-white')
            if(data.StatusCharge.trim() == '00 No charging') {
                $('#ctn_pv').addClass('bg-light text-dark')
                $('.pvicon').addClass('fa-moon')
            } else {
                $('#ctn_pv').addClass('bg-warning text-dark')
                $('.pvicon').addClass('fa-sun')
            }

            $('#headerstartdate').text(moment(datajson.generated.start).format('HH:mm'));
            $('#headerenddate').text(moment(datajson.generated.end).format('HH:mm'));

//            $('#generatedend').text(moment(datajson.generated.start).format('HH:mm:ss') + ' às '
//                + moment(datajson.generated.end).format('HH:mm:ss'))


//            var ctx = $("#myChart");
//            var myChart = new Chart(ctx, {
//            type: 'bar',
//                data: {
//                    labels: ["Med", "Max", "Min", "Total"],
//                    datasets: [{
//                        label: 'Potência',
//                        data: [datajson.generated.power.avg,
//                        datajson.generated.power.max, datajson.generated.power.min, datajson.generated.power.total],
//                        borderWidth: 1
//                    }]
//                },
//                options: {
//                    scales: {
//                        yAxes: [{
//                            ticks: {
//                                beginAtZero:true
//                            }
//                        }]
//                    }
//                }
//            });

            $('#headerload').text(data.StatusDischarging)
            $('#headerbatterysystem').text(data.VoltageSystemBattery + 'V')
            $('#headerbatterystatus').text(get_status_battery(data.StatusBattery))
            $('#headerbatterycharge').text(get_status_charge(data.StatusCharge))

            gaugevolt.set(data.pv.voltage);
            gaugecurrent.set(data.pv.current);
            gaugepower.set(data.pv.power);
            gaugepowertotal.set(datajson.generated.power.total);

            gaugebatteryvolt.set(data.battery.voltage);
            gaugebatterycurrent.set(data.battery.current);
            gaugebatterypower.set(data.battery.power);
            gaugebatterysoc.set(data.BatterySOC);
            gaugetemperature.set(data.temperature.Battery);
            gaugeremote.set(data.temperature.RemoteBattery);

            gaugedischargingvolt.set(data.discharging.voltage);
            gaugedischargingcurrent.set(data.discharging.current);
            gaugedischargingpower.set(data.discharging.power);

            gaugetemperatureinside.set(data.temperature.InsideEquipment);
            gaugetemperaturecomponent.set(data.temperature.PowerComponents);
        });
    }
    get_data()
    window.setInterval(get_data, 5000);

    var opts = {
        angle: -0.1, // The span of the gauge arc
        lineWidth: 0.2, // The line thickness
        radiusScale: 1, // Relative radius
        pointer: {
            length: 0.65, // // Relative to gauge radius
            strokeWidth: 0.055, // The thickness
            color: '#FFF' // Fill color
        },
        limitMax: false,     // If false, max value increases automatically if value > maxValue
        limitMin: false,     // If true, the min value of the gauge will be fixed
        colorStart: '#6FADCF',   // Colors
        colorStop: '#8FC0DA',    // just experiment with them
        strokeColor: '#E0E0E0',  // to see which ones work best for you
        generateGradient: true,
        highDpiSupport: true,     // High resolution support
        percentColors: [[0.0, "#ff0000" ], [0.50, "#f9c802"], [1.0, "#a9d70b"]],

        renderTicks: {
          divisions: 5,
          divWidth: 1.1,
          divLength: 0.7,
          divColor: "#333333",
          subDivisions: 3,
          subLength: 0.5,
          subWidth: 0.6,
          subColor: "#666666"
        },

//        staticZones: [
//           {strokeStyle: "#F03E3E", min: 0, max: 15  }, // Red from 100 to 130
//           {strokeStyle: "#FFDD00", min: 15, max: 30 }, // Yellow
//           {strokeStyle: "#30B32D", min: 30, max: 50 }, // Green
//        ],

//        staticLabels: {
//          font: "8px sans-serif",  // Specifies font
//          labels: [0, 15, 30, 5],  // Print labels at these values
//          color: "#000000",  // Optional: Label text color
//          fractionDigits: 0  // Optional: Numerical precision. 0=round off.
//        },
    };

//    var target = document.getElementById('canvas-preview'); // your canvas element
//    var gauge = new Gauge(target).setOptions(opts); // create sexy gauge!
//    gauge.setTextField(document.getElementById("preview-textfield"));

    var CustomTextRenderer = function(el) {
        this.el = el;
        this.render = function(gauge) {
            this.el.innerHTML = gauge.displayedValue.toFixed(2);
        }
    }
    CustomTextRenderer.prototype = new TextRenderer();

    var gaugevolt = new Gauge(document.getElementById("canvas-volt"));
    opts.staticZones= [
       {strokeStyle: "#F03E3E", min: 0, max: 15  },
       {strokeStyle: "#FFDD00", min: 15, max: 24 },
       {strokeStyle: "#30B32D", min: 24, max: 100 },
    ];
    gaugevolt.setOptions(opts);
    gaugevolt.setTextField(new CustomTextRenderer(document.getElementById("volt-textfield")))
    gaugevolt.maxValue = 100.0;
    gaugevolt.setMinValue(0.0);
    gaugevolt.animationSpeed = 32;

    opts.staticZones = [
       {strokeStyle: "#30B32D", min: 0, max: 5  }, // Red from 100 to 130
       {strokeStyle: "#FFDD00", min: 5, max: 15 }, // Yellow
       {strokeStyle: "#F03E3E", min: 15, max: 40 }, // Green
    ];
    var gaugecurrent = new Gauge(document.getElementById("canvas-current"));
    gaugecurrent.setOptions(opts);
    gaugecurrent.setTextField(new CustomTextRenderer(document.getElementById("current-textfield")))
    gaugecurrent.maxValue = 40.0;
    gaugecurrent.setMinValue(0.0);
    gaugecurrent.animationSpeed = 32;

    opts.staticZones = undefined;
    var gaugepower = new Gauge(document.getElementById("canvas-power"));
    gaugepower.setOptions(opts);
    gaugepower.setTextField(new CustomTextRenderer(document.getElementById("power-textfield")))
    gaugepower.maxValue = 1040.0;
    gaugepower.setMinValue(0.0);
    gaugepower.animationSpeed = 32;

    opts.staticZones = undefined;
    var gaugepowertotal = new Gauge(document.getElementById("canvas-powertotal"));
    gaugepowertotal.setOptions(opts);
    gaugepowertotal.setTextField(new CustomTextRenderer(document.getElementById("powertotal-textfield")))
    gaugepowertotal.maxValue = 5000.0;
    gaugepowertotal.setMinValue(0.0);
    gaugepowertotal.animationSpeed = 32;

    opts.staticZones = [
       {strokeStyle: "#F03E3E", min: 9, max: 21.2  }, // Red from 100 to 130
       {strokeStyle: "#FFDD00", min: 21.2, max: 25.2 }, // Yellow
       {strokeStyle: "#30B32D", min: 25.2, max: 30 }, // Green
       {strokeStyle: "#F03E3E", min: 30, max: 36 }, // Green
    ];
    var gaugebatteryvolt = new Gauge(document.getElementById("canvas-batteryvolt"));
    gaugebatteryvolt.setOptions(opts);
    gaugebatteryvolt.setTextField(new CustomTextRenderer(document.getElementById("batteryvolt-textfield")))
    gaugebatteryvolt.maxValue = 36.0;
    gaugebatteryvolt.setMinValue(9);
    gaugebatteryvolt.animationSpeed = 32;

    opts.staticZones = [
       {strokeStyle: "#30B32D", min: 0, max: 5  }, // Red from 100 to 130
       {strokeStyle: "#FFDD00", min: 5, max: 15 }, // Yellow
       {strokeStyle: "#F03E3E", min: 15, max: 40 }, // Green
    ];
    var gaugebatterycurrent = new Gauge(document.getElementById("canvas-batterycurrent"));
    gaugebatterycurrent.setOptions(opts);
    gaugebatterycurrent.setTextField(new CustomTextRenderer(document.getElementById("batterycurrent-textfield")))
    gaugebatterycurrent.maxValue = 40.0;
    gaugebatterycurrent.setMinValue(0.0);
    gaugebatterycurrent.animationSpeed = 32;

    opts.staticZones = undefined;
    var gaugebatterypower = new Gauge(document.getElementById("canvas-batterypower"));
    gaugebatterypower.setOptions(opts);
    gaugebatterypower.setTextField(new CustomTextRenderer(document.getElementById("batterypower-textfield")))
    gaugebatterypower.maxValue = 1000.0;
    gaugebatterypower.setMinValue(0.0);
    gaugebatterypower.animationSpeed = 32;

    opts.staticZones = [
       {strokeStyle: "#F03E3E", min: 0, max: 33  }, // Red from 100 to 130
       {strokeStyle: "#FFDD00", min: 33, max: 66 }, // Yellow
       {strokeStyle: "#30B32D", min: 66, max: 100 }, // Green
    ];
    var gaugebatterysoc = new Gauge(document.getElementById("canvas-batterysoc"));
    gaugebatterysoc.setOptions(opts);
    gaugebatterysoc.setTextField(document.getElementById("batterysoc-textfield"))
    gaugebatterysoc.maxValue = 100.0;
    gaugebatterysoc.setMinValue(0.0);
    gaugebatterysoc.animationSpeed = 32;

    opts.staticZones = [
       { strokeStyle: "#EEEEE", min: 0, max: 25  }, // Red from 100 to 130
       { strokeStyle: "#FFDD00", min: 25, max: 45 }, // Yellow
       { strokeStyle: "#F03E3E", min: 45, max: 60 }, // Green
    ];
    var gaugetemperature = new Gauge(document.getElementById("canvas-temperature"));
    gaugetemperature.setOptions(opts);
    gaugetemperature.setTextField(document.getElementById("temperature-textfield"))
    gaugetemperature.maxValue = 60.0;
    gaugetemperature.setMinValue(0.0);
    gaugetemperature.animationSpeed = 32;

    opts.staticZones = [
       { strokeStyle: "#EEEEE", min: 0, max: 25  }, // Red from 100 to 130
       { strokeStyle: "#FFDD00", min: 25, max: 45 }, // Yellow
       { strokeStyle: "#F03E3E", min: 45, max: 60 }, // Green
    ];
    var gaugeremote = new Gauge(document.getElementById("canvas-remote"));
    gaugeremote.setOptions(opts);
    gaugeremote.setTextField(new CustomTextRenderer(document.getElementById("remote-textfield")))
    gaugeremote.maxValue = 60.0;
    gaugeremote.setMinValue(0.0);
    gaugeremote.animationSpeed = 32;


    opts.staticZones = [
       { strokeStyle: "#EEEEE", min: 0, max: 25  }, // Red from 100 to 130
       { strokeStyle: "#FFDD00", min: 25, max: 45 }, // Yellow
       { strokeStyle: "#F03E3E", min: 45, max: 60 }, // Green
    ];
    var gaugetemperatureinside = new Gauge(document.getElementById("canvas-inside"));
    gaugetemperatureinside.setOptions(opts);
    gaugetemperatureinside.setTextField(new CustomTextRenderer(document.getElementById("inside-textfield")))
    gaugetemperatureinside.maxValue = 60.0;
    gaugetemperatureinside.setMinValue(0.0);
    gaugetemperatureinside.animationSpeed = 32;

    opts.staticZones = [
       { strokeStyle: "#EEEEE", min: 0, max: 25  }, // Red from 100 to 130
       { strokeStyle: "#FFDD00", min: 25, max: 45 }, // Yellow
       { strokeStyle: "#F03E3E", min: 45, max: 60 }, // Green
    ];
    var gaugetemperaturecomponent = new Gauge(document.getElementById("canvas-component"));
    gaugetemperaturecomponent.setOptions(opts);
    gaugetemperaturecomponent.setTextField(new CustomTextRenderer(document.getElementById("component-textfield")))
    gaugetemperaturecomponent.maxValue = 60.0;
    gaugetemperaturecomponent.setMinValue(0.0);
    gaugetemperaturecomponent.animationSpeed = 32;

    var gaugedischargingvolt = new Gauge(document.getElementById("canvas-dischargingvolt"));
   opts.staticZones = [
       {strokeStyle: "#F03E3E", min: 9, max: 21.2  }, // Red from 100 to 130
       {strokeStyle: "#FFDD00", min: 21.2, max: 25.2 }, // Yellow
       {strokeStyle: "#30B32D", min: 25.2, max: 30 }, // Green
       {strokeStyle: "#F03E3E", min: 30, max: 36 }, // Green
    ];
    gaugedischargingvolt.setOptions(opts);
    gaugedischargingvolt.setTextField(new CustomTextRenderer(document.getElementById("dischargingvolt-textfield")))
    gaugedischargingvolt.maxValue = 36.0;
    gaugedischargingvolt.setMinValue(9.0);
    gaugedischargingvolt.animationSpeed = 32;

    opts.staticZones = [
       {strokeStyle: "#30B32D", min: 0, max: 5  }, // Red from 100 to 130
       {strokeStyle: "#FFDD00", min: 5, max: 15 }, // Yellow
       {strokeStyle: "#F03E3E", min: 15, max: 40 }, // Green
    ];
    var gaugedischargingcurrent = new Gauge(document.getElementById("canvas-dischargingcurrent"));
    gaugedischargingcurrent.setOptions(opts);
    gaugedischargingcurrent.setTextField(new CustomTextRenderer(document.getElementById("dischargingcurrent-textfield")))
    gaugedischargingcurrent.maxValue = 40.0;
    gaugedischargingcurrent.setMinValue(0.0);
    gaugedischargingcurrent.animationSpeed = 32;

    opts.staticZones = undefined;
    var gaugedischargingpower = new Gauge(document.getElementById("canvas-dischargingpower"));
    gaugedischargingpower.setOptions(opts);
    gaugedischargingpower.setTextField(new CustomTextRenderer(document.getElementById("dischargingpower-textfield")))
    gaugedischargingpower.maxValue = 1000.0;
    gaugedischargingpower.setMinValue(0.0);
    gaugedischargingpower.animationSpeed = 32;


    $.get(url_context + 'device/grouphourredirect', function(datajson) {
        console.log(datajson)

        labels = []
        datajson.forEach(function (item) {
          labels.push(parseInt(new Date(item.CreatedDate).getHours()));
        })

        new Chart(document.getElementById("myChart"), {
          type: 'line',
          data: {
            labels: labels,
            datasets: [{
                data: [86,114,106,106,107,111,133,221,783,2478],
                label: "Tensão",
                borderColor: "#3e95cd",
                fill: false
              }, {
                data: [282,350,411,502,635,809,947,1402,3700,5267],
                label: "Corrente",
                borderColor: "#8e5ea2",
                fill: false
              }, {
                data: [168,170,178,190,203,276,408,547,675,734],
                label: "Potência",
                borderColor: "#3cba9f",
                fill: false
              }, {
                data: [40,20,10,16,24,38,74,167,508,784],
                label: "SOC",
                borderColor: "#e8c3b9",
                fill: false
              }
            ]
          },
          options: {
            title: {
              display: true,
              text: 'World population per region (in millions)'
            }
          }
        });
    })

});