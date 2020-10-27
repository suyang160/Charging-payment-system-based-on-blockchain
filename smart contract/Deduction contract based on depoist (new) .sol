pragma solidity >=0.5.0 <0.7.0;
//合约需要有一个计费函数，该计费函数的参数可以被设置，但只能被合约的创建者即充电桩厂商进行设置。
//第一步:createOrder 设置该合约的控制者，即充电桩以及电动汽车的钱包地址
//

contract Order{
    address  payable public order_CP;
    address  payable public order_EV;
    address  payable public order_CP_global;
    address payable public government;
    //时间单位S
    uint256 startTimeByEV;
    uint256 startTimeByCP;
    uint256 endTimeByEV;
    uint256 endTimeByCP;
    //实际值*10 KW.h
    uint256 chargingPowerByEV;
    uint256 chargingPowerByCP;
    uint256 chargingPowerUnitPrice;
    uint256 lock_startTime;
    uint256 lock_maxTime = 604800;
    enum order_state{
        normal,
        abnormal
    }
    order_state public now_state;
    

    modifier onlyCP() 
    {
        require(
            msg.sender == order_CP,
            "Only CP of this order can call this."
        ); 
         _;
    }

    modifier onlyEV() 
    {
        require(
            msg.sender == order_EV,
            "Only EV of this order can call this."
        ); 
        _;
    }

    modifier onlyEVorCP() 
    {
        require(
            msg.sender == order_EV || msg.sender == order_CP,
            "Only EV of this order can call this."
        );
        _;
    }

    modifier startTimeNotZero()
    {
        require(
            startTimeByEV !=0 && startTimeByCP != 0,
            "The startTimeByEV and startTimeByCP cannot be zero."
        );
        _;
    }

    modifier chargingPowerNotZero()
    {
        require(
            chargingPowerByEV !=0 && chargingPowerByCP != 0,
            "The chargingPowerByEV and chargingPowerByCP cannot be zero."
        );
        _;
    }


    constructor (address payable CP, address payable EV, uint256 _chargingPowerUnitPrice, address payable _government,address payable _order_CP_global) public payable{
        order_CP = CP;
        order_EV = EV;
        chargingPowerUnitPrice = _chargingPowerUnitPrice;
        government = _government;
        order_CP_global = _order_CP_global;
    }

    function calculate_absolute_difference(uint256 value1, uint256 value2) public
    returns (uint256 result)
    {
        if(value1 >= value2)
        {
            return value1-value2;
        }
        else
        {
            return value2-value1;
        }
    }
    //起始时间确认异常
    function exception_of_startTime()
    public
    payable
    startTimeNotZero()
    onlyEVorCP() 
    {
        if(calculate_absolute_difference(startTimeByEV,startTimeByCP) > 60)
        {
            address temp = address(this);
            order_EV.transfer(temp.balance);
        }
    }

    //正常结束or异常结束
    //正常返回，异常等待操作，解锁，时间到期后，token转入政府账户。
    function endTheCharging()
    public
    onlyEVorCP()
    returns (bool result) 
    {
        if(calculate_absolute_difference(chargingPowerByEV,chargingPowerByCP) <=1)
        {
            address temp = address(this);
            order_CP_global.transfer(calculate_chargingfee(chargingPowerByCP));
            order_EV.transfer(temp.balance);
            return true;
        }
        else
        {
            now_state = order_state.abnormal;
            lock_startTime = now;
            return false;
        }
    }

    function transferToGovernment()
    public
    returns (bool result)
    {
        address temp = address(this);
        if(now_state == order_state.abnormal)
        {
            if(now-lock_startTime > lock_maxTime)
            {
                government.transfer(temp.balance);
            }
        }
    }




    //计算充电费用
    function calculate_chargingfee(uint256 chargingPower)
    public
    returns (uint256 result)
    {
        return chargingPower*chargingPowerUnitPrice;
    }

    //返回当前合约所拥有的余额
    function getBalance() public view returns (uint256 result) 
    {
        return address(this).balance;
    }



    //返回相应的变量
    function get_startTimeByEV() public view returns (uint result)
    {
        return startTimeByEV;
    }

    function get_startTimeByCP() public view returns (uint result)
    {
        return startTimeByCP;
    }

    function get_endTimeByEV() public view returns (uint result)
    {
        return endTimeByEV;
    }

    function get_endTimeByCP() public view returns (uint result)
    {
        return endTimeByCP;
    }

    function get_chargingPowerByEV() public view returns (uint result)
    {
        return chargingPowerByEV;
    }



    //设置相应的变量
    function confirmChargingStartbyCP(uint256 _startTimeByCP) 
    public
    onlyCP() 
    {
        startTimeByCP = _startTimeByCP;
    }

    function confirmChargingStartbyEV(uint256 _startTimeByEV) 
    public
    onlyEV() 
    {
        startTimeByEV = _startTimeByEV;
    }

    function confirmChargingEndbyCP(uint256 _endTimeByCP) 
    public
    onlyCP() 
    {
        endTimeByCP = _endTimeByCP;
    }

    function confirmChargingEndbyEV(uint256 _endTimeByEV) 
    public
    onlyEV() 
    {
        endTimeByEV = _endTimeByEV;
    }

    function confirmChargingPowerByCP(uint256 _chargingPowerByCP)
    public
    onlyCP()
    {
        chargingPowerByCP = _chargingPowerByCP;
    }

    function confirmChargingPowerByEV(uint256 _chargingPowerByEV)
    public
    onlyEV()
    {
        chargingPowerByEV = _chargingPowerByEV;
    }

}


contract ChargingFeeDeduction{
    uint256 orderID;
    address owner;
    address payable government;
    address payable CP_global;
    uint256 chargingPowerUnitPrice;
    Order [1000000] allOrder;
    uint256 orderindex = 0;
   
    modifier onlyOwner() 
    {
        require(
            msg.sender == owner,
            "Only owner can call this."
        );
        _;
    }
    constructor () public payable
    {
        owner = msg.sender;
    }

    function createOrder(address payable CP,address payable EV)
    public
    returns (Order result)
    {
        Order order = new Order(CP,EV,chargingPowerUnitPrice,government,CP_global);
        allOrder[orderindex] = order;
        orderindex++;
        return order;
    }

    function setGovernmentAddress(address payable newGovernmentaddress)
    public
    onlyOwner() 
    returns (bool result)
    {
        government = newGovernmentaddress;
        return true;
    }

    function setCPglobalAddress(address payable newCPglobalAddress)
    public
    onlyOwner()
    returns (bool result)
    {
        CP_global = newCPglobalAddress;
        return true;
    }

    function setChargingPowerUnitPrice(uint256 newChargingPowerUnitPrice)
    public
    onlyOwner()
    returns (bool result)
    {
        chargingPowerUnitPrice = newChargingPowerUnitPrice;
        return true;
    }
}