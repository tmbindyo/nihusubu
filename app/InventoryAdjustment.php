<?php

namespace App;

use App\Traits\UuidTrait;
use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\SoftDeletes;

class InventoryAdjustment extends Model
{
    use SoftDeletes, UuidTrait;
    public $incrementing = false;

    // Parents
    public function status()
    {
        return $this->belongsTo('App\Status');
    }
    public function user()
    {
        return $this->belongsTo('App\User');
    }
    public function account()
    {
        return $this->belongsTo('App\Account');
    }
    public function warehouse()
    {
        return $this->belongsTo('App\Warehouse');
    }
    public function reason()
    {
        return $this->belongsTo('App\Reason');
    }

    // Children
    public function inventory_adjustment_products()
    {
        return $this->hasMany('App\InventoryAdjustmentProduct');
    }
}
