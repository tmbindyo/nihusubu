<?php

namespace App;

use App\Traits\UuidTrait;
use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\SoftDeletes;

class Currency extends Model
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

    // Children
    public function institutions()
    {
        return $this->hasMany('App\Institution');
    }
    public function contacts()
    {
        return $this->hasMany('App\Contact');
    }
    public function expenses()
    {
        return $this->hasMany('App\Expense');
    }
    public function manual_journals()
    {
        return $this->hasMany('App\ManualJournal');
    }
    public function purchase_orders()
    {
        return $this->hasMany('App\PurchaseOrder');
    }
}
